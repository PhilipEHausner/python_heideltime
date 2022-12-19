#    Python Wrapper to call HeidelTime-standalone from Python
#    Copyright (C) 2019-2022  Philip Hausner
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import subprocess
import tempfile
import regex
import os
from typing import List, Dict, Optional, Union

from bs4 import BeautifulSoup

from .config_Heideltime import Heideltime_path

# Taken from the documentation linked below
AVAILABLE_LANGUAGES = ['ARABIC', 'CHINESE', 'CROATIAN', 'DUTCH', 'ENGLISH', 'ENGLISHCOLL', 'ENGLISHSCI', 'ESTONIAN',
                       'FRENCH', 'GERMAN', 'ITALIAN', 'PORTUGUESE', 'RUSSIAN', 'SPANISH', 'VIETNAMESE']

AVAILABLE_DOCUMENT_TYPES = ['COLLOQUIAL', 'NARRATIVES', 'NEWS', 'SCIENTIFIC']
AVAILABLE_OUTPUT_TYPES = ['JSON', 'TIMEML', 'XMI']  # TODO: Add JSON output by parsing XML from Heideltime


class Heideltime:

    heidel_path: str
    document_time: Optional[str]
    language: str
    doc_type: str
    otuput_type: str
    encoding: str
    config_file: str
    output_json: bool
    verbosity: bool
    interval_tagger: bool
    local: Optional[str]
    pos_tagger: Optional[str]

    def __init__(self) -> None:
        """
        Initializes the most important settings to sensible default values.
        For further parameter explanations, see the documentation for the Heideltime standaloe application here:
        https://gate.ac.uk/gate/plugins/Tagger_GATE-Time/doc/HeidelTime-Standalone-Manual.pdf
        """
        # assure that path to HeidelTime is in the correct format
        if Heideltime_path is None:
            raise ValueError('Please specify the path to HeidelTime-standalone in config_Heideltime.py.')
        elif Heideltime_path[-1] == '/':
            self.heidel_path = Heideltime_path[:-1]
        else:
            self.heidel_path = Heideltime_path

        # Set reasonable default parameters
        self.document_time = None
        self.language = 'ENGLISH'
        self.doc_type = 'NARRATIVES'
        self.output_type = 'TIMEML'
        self.encoding = 'UTF-8'
        self.config_file = os.path.join(self.heidel_path, 'config.props')

        self.output_json = False

        # these features are not tested and might not work
        self.verbosity = False
        self.interval_tagger = False
        self.locale = None
        self.pos_tagger = None

    # FIXME: called document creation time or dct in HeidelTime, consider updating naming
    def set_document_time(self, document_time: str) -> None:
        """
        Expects a string in the form of 'YYYY-MM-DD' to specify the document creation time (DCT).
        Only used in combination with 'NEWS' or 'COLLOQUIAL' document types.
        """
        if not regex.match(r'[0-9]{4}-[0-9]{2}-[0-9]{2}', document_time):
            raise ValueError('Incorrect format for document time specified. Please use the \"YYYY-MM-DD\" format.')
        self.document_time = document_time

    def set_language(self, language: str) -> None:
        """
        Sets the language of the parser. Available languages according to Heideltime docs are:
        'ARABIC', 'CHINESE', 'CROATIAN', 'DUTCH', 'ENGLISH', 'ENGLISHCOLL' (for -t COLLOQUIAL),
        'ENGLISHSCI' (for -t SCIENTIFIC), 'ESTONIAN', 'FRENCH', 'GERMAN', 'ITALIAN', 'PORTUGUESE', 'RUSSIAN',
        'SPANISH', 'VIETNAMESE'
        """
        if not language.upper() in AVAILABLE_LANGUAGES:
            raise ValueError(f'Unknown language "{language}" specified! '
                             f'Please specify one of the supported languages below:\n{AVAILABLE_LANGUAGES}')
        self.language = language.upper()

    def set_document_type(self, doc_type: str) -> None:
        """
        Sets the document type. Can be either of 'COLLOQUIAL', 'NARRATIVES', 'NEWS', or 'SCIENTIFIC'.
        """
        if not doc_type.upper() in AVAILABLE_DOCUMENT_TYPES:
            raise ValueError(f'Unknown document type "{doc_type}" specified! '
                             f'Please use one of the following supported document types: {AVAILABLE_DOCUMENT_TYPES}')
        self.doc_type = doc_type.upper()

    def set_output_type(self, output_type) -> None:
        """
        Set the output type of the parser. Heideltime supports either of 'TIMEML' or 'XMI', and defaults to the former.
        If 'JSON' is selected, internally it will use 'TIMEML', and parse the output here.
        """
        if not output_type.upper() in AVAILABLE_OUTPUT_TYPES:
            raise ValueError(f'Unknown output type "{output_type}" specified! '
                             f'Please use one of the following supported output types: {AVAILABLE_OUTPUT_TYPES}')
        # Internally handle JSON differently.
        if output_type.upper() == 'JSON':
            self.output_json = True
            self.output_type = 'TIMEML'
        else:
            self.output_type = output_type.upper()

    def set_encoding(self, encoding: str) -> None:
        """
        Set the corresponding output encoding used by Heideltime. It is unclear from the original docs,
        which exact encodings are supported.
        """
        self.encoding = encoding

    def set_config_file(self, config_file: str) -> None:
        """
        Set the path of Heideltime config file. Requires a full (absolute) path.
        """
        self.config_file = config_file

    # FIXME: Technically, Heideltime supports two different verbosity levels, which we cannot model here.
    #  The supported options are either -v or -vv, where I assume -vv is a "more verbose" verbose option.
    def set_verbosity(self, verbosity: bool) -> None:
        self.verbosity = verbosity

    def set_interval_tagger(self, interval_tagger: bool) -> None:
        self.interval_tagger = interval_tagger

    def set_locale(self, locale: str) -> None:
        self.locale = locale

    def set_pos_tagger(self, pos_tagger: str) -> None:
        self.pos_tagger = pos_tagger

    def parse(self, document: str) -> Union[str, List[Dict]]:
        # temporary file since HeidelTime standalone needs input file
        temp = tempfile.NamedTemporaryFile()
        temp.write(document.encode('utf-8'))
        temp.flush()
        # create string to execute in bash shell
        inputs = ['java', '-jar', self.heidel_path + '/de.unihd.dbs.heideltime.standalone.jar',
                  '-l', self.language, '-t', self.doc_type, '-o', self.output_type,
                  '-c', self.config_file, '-e', self.encoding]
        # add all optional arguments
        if self.document_time:
            inputs.append('-dct')
            inputs.append(self.document_time)
        if self.verbosity:
            inputs.append('-v')
        if self.interval_tagger:
            inputs.append('-it')
        if self.locale:
            inputs.append('-locale')
            inputs.append(self.locale)
        if self.pos_tagger:
            inputs.append('-pos')
            inputs.append(self.pos_tagger)
        # lastly append the temporary file
        inputs.append(temp.name)
        # execute string in the bash shell
        heideltime_result = subprocess.check_output(inputs).decode('utf-8')
        if self.output_json:
            return self._convert_to_json(heideltime_result)
        else:
            return heideltime_result

    @staticmethod
    def _convert_to_json(xml_text: str) -> List[Dict]:
        """
        Converts tagged texts into JSON-like objects, where individual temporal tags are identified based on the
        extracted attributes, as well as an exact character position in the raw text.
        """

        soup = BeautifulSoup(xml_text)

        try:
            content = soup.findAll("timeml")[0]
        except IndexError:
            raise IndexError('Could not process output from Heideltime! Please verify that your output is correct '
                             'by running with output_type = "TIMEML"')

        # Removes additional newlines added by Heideltime's XML output.
        # This does not use .strip("\n"), because the original text could in theory contain newlines already
        # TODO: Write test case to verify behavior of strip vs our method
        remaining_raw_text = content.text[1:-1]
        offset = 0
        tags = content.findAll("timex3")

        json_tags = []
        for tag in tags:
            json_tags.append(tag.attrs)
            json_tags[-1]["text"] = tag.text
            # Also store the character position within the raw text
            start_idx = remaining_raw_text.find(tag.text) + offset
            end_idx = start_idx + len(tag.text)
            json_tags[-1]["char_pos"] = [start_idx, end_idx]

            # To avoid finding tags with the exact same content
            cut_length = remaining_raw_text.find(tag.text) + len(tag.text)
            offset += cut_length
            remaining_raw_text = remaining_raw_text[cut_length:]

        return json_tags
