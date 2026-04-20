import platform
import sys

from sc_foundation import DateHelper, SCConfigManager, SCLogger

from example_config_schemas import ConfigSchema

CONFIG_FILE = "example_config.yaml"


def main():
    """Main function to run the example code."""
    print(f"Hello from sc-foundation running on {platform.system()}")

    # Get our default schema, validation schema, and placeholders
    schemas = ConfigSchema()

    # Initialize the SC_ConfigManager class
    try:
        config = SCConfigManager(
            config_file=CONFIG_FILE,
            default_config=schemas.default,
            validation_schema=schemas.validation,
            placeholders=schemas.placeholders
        )
    except RuntimeError as e:
        print(f"Configuration file error: {e}", file=sys.stderr)
        return

    # Print a value from the sample config file
    print(f"API key = {config.get('AmberAPI', 'APIKey')}")

    # Initialize the SC_Logger class
    try:
        logger = SCLogger(config.get_logger_settings())
    except RuntimeError as e:
        print(f"Logger initialisation error: {e}", file=sys.stderr)
        return

    logger.log_message("This is a test message at the summary level.", "summary")

    # Setup email
    email_settings = config.get_email_settings()

    if email_settings is not None:
        logger.register_email_settings(email_settings)

        text_msg = "Hello world from sc-foundation example code."
        if logger.send_email("Hello world", text_msg):
            logger.log_message("Email sent OK.", "detailed")

    # Use DateHelper to get the current date and time
    prior_date = DateHelper.today_add_days(-7)
    print(f"Prior date (7 days ago): {prior_date}")

    # See if we have a fatal error from a previous run
    if logger.get_fatal_error():
        print("Prior fatal error detected.")
        logger.clear_fatal_error()


if __name__ == "__main__":
    main()
