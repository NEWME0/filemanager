import dotenv
import secrets
import argparse


DOT_ENV_PATH = '.env'


def command_help(parser_instance):
    """ Print parser's help """
    def wrapper(args):
        parser_instance.print_help()

    return wrapper


def command_api_key_name(args):
    """ Get or set API_KEY_NAME """
    if args.default:
        dotenv.set_key(DOT_ENV_PATH, key_to_set='API_KEY_NAME', value_to_set='access-token')

    if args.set:
        dotenv.set_key(DOT_ENV_PATH, key_to_set='API_KEY_NAME', value_to_set=args.set)

    print(dotenv.get_key(DOT_ENV_PATH, 'API_KEY_NAME'))


def command_api_key_value(args):
    """ Get or set API_KEY_VALUE """
    if args.generate:
        api_key = secrets.token_urlsafe(args.length)
        dotenv.set_key(DOT_ENV_PATH, key_to_set='API_KEY_VALUE', value_to_set=api_key)

    if args.set:
        dotenv.set_key(DOT_ENV_PATH, key_to_set='API_KEY_VALUE', value_to_set=args.set)

    print(dotenv.get_key(DOT_ENV_PATH, 'API_KEY_VALUE'))


def command_api_key_domain(args):
    """ Get or set API_KEY_DOMAIN """
    if args.default:
        dotenv.set_key(DOT_ENV_PATH, key_to_set='API_KEY_DOMAIN', value_to_set='localhost')

    if args.set:
        dotenv.set_key(DOT_ENV_PATH, key_to_set='API_KEY_DOMAIN', value_to_set=args.set)

    print(dotenv.get_key(DOT_ENV_PATH, 'API_KEY_DOMAIN'))


if __name__ == '__main__':
    # Init parser
    parser = argparse.ArgumentParser()

    # Setup default command
    parser.set_defaults(func=command_help(parser))

    # Init subparsers
    commands = parser.add_subparsers()

    # Setup api_key_name command
    api_key_name = commands.add_parser('api_key_name', help="Get or set API_KEY_NAME")
    api_key_name.add_argument('--default', action='store_true', help="Set default value (access-token)")
    api_key_name.add_argument('--set', help="Set new value")
    api_key_name.set_defaults(func=command_api_key_name)

    # Setup api_key_value command
    api_key_value = commands.add_parser('api_key_value', help="Get or set API_KEY_VALUE")
    api_key_value.add_argument('--generate', action='store_true', help='Generate new value')
    api_key_value.add_argument('--length', default=50, type=int, help="Set length (default=50)")
    api_key_value.add_argument('--set', help="Set new value")
    api_key_value.set_defaults(func=command_api_key_value)

    # Setup api_key_domain command
    api_key_domain = commands.add_parser('api_key_domain', help="Get or set API_KEY_DOMAIN")
    api_key_domain.add_argument('--default', action='store_true', help="Set default value (localhost)")
    api_key_domain.add_argument('--set', help="Set new value")
    api_key_domain.set_defaults(func=command_api_key_domain)

    # Parse arguments and call specified command
    arguments = parser.parse_args()
    arguments.func(arguments)
