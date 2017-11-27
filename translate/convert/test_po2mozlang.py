# -*- coding: utf-8 -*-

from translate.convert import po2mozlang, test_convert
from translate.misc import wStringIO
from translate.storage import po


class TestPO2Lang(object):

    def po2lang(self, input_string):
        """helper that converts po source to .lang source without requiring files"""
        inputfile = wStringIO.StringIO(input_string)
        inputpo = po.pofile(inputfile)
        convertor = po2mozlang.po2lang(mark_active=False)
        outputlang = convertor.convertstore(inputpo)
        return bytes(outputlang).decode('utf-8')

    def test_simple(self):
        """check the simplest case of merging a translation"""
        input_string = """#: prop
msgid "Source"
msgstr "Target"
"""
        expected_output = """;Source
Target


"""
        assert expected_output == self.po2lang(input_string)

    def test_comment(self):
        """Simple # comments"""
        input_string = """#. Comment
#: prop
msgid "Source"
msgstr "Target"
"""
        expected_output = """# Comment
;Source
Target


"""
        assert expected_output == self.po2lang(input_string)

    def test_fuzzy(self):
        """What happens with a fuzzy string"""
        input_string = """#. Comment
#: prop
#, fuzzy
msgid "Source"
msgstr "Target"
"""
        expected_output = """# Comment
;Source
Source


"""
        assert expected_output == self.po2lang(input_string)

    def test_ok_marker(self):
        """The {ok} marker"""
        input_string = """#: prop
msgid "Same"
msgstr "Same"
"""
        expected_output = """;Same
Same {ok}


"""
        assert expected_output == self.po2lang(input_string)


class TestPO2LangCommand(test_convert.TestConvertCommand, TestPO2Lang):
    """Tests running actual po2prop commands on files"""
    convertmodule = po2mozlang
    defaultoptions = {"progress": "none"}

    def test_help(self):
        """tests getting help"""
        options = test_convert.TestConvertCommand.test_help(self)
        options = self.help_check(options, "-t TEMPLATE, --template=TEMPLATE")
        options = self.help_check(options, "--threshold=PERCENT")
        options = self.help_check(options, "--fuzzy")
        options = self.help_check(options, "--mark-active")
        options = self.help_check(options, "--nofuzzy", last=True)
