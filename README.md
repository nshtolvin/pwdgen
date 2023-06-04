# pwdgwn

The project of a simple console password generator.

## Capability
In this application, you can generate a password based on English dictionary words with delimiters and/or prefixes. There are 4 levels of complexity of created passwords:
1. weak
2. normal
3. strong
4. custom

### Custom passwords
Unlike "standard" passwords, the parameters of which are stored in the program, the parameters of a custom (user) password can be set manually. To do this, you can use menu (item 6) or you can edit the configuration file [conf.ini](conf.ini).

When editing [conf.ini](conf.ini), it is only allowed to change the parameter values:
- words_count - an integer in the range 2..6
- char_count - an integer in the range 3..5
- use_numbers - True/False
- use_special - True/False
- use_upper_case - True/False

Deleting or changing a parameter, entering a parameter value outside of the allowed values, will result in the use of the default parameters.

## Requirements (Installation)
You need the [following](requirements.txt) libraries to use the project.
