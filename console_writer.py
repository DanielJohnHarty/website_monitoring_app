import os


DASHBOARD_WIDTH = 50


class WebPerformanceDashboard:
    """
    The WebPerformanceDashboard is the producer of
    content to be written to the console. No stats or
    complex text formatting here.
    """

    def __init__(self):

        self.data = {}
        self.persisted_messages = []

        # Convert seconds to minutes. Returns positive int.
        self.secToMin = lambda seconds: abs(int(seconds / 60))

    def yield_persisted_messages(self):
        """
        Persisted messages can be alerts
        to be printed to the report 
        indefinitely
        """
        yield "_" * DASHBOARD_WIDTH
        yield "Alert History"
        yield "_" * DASHBOARD_WIDTH

        if self.persisted_messages:
            for msg in self.persisted_messages:
                yield msg
        else:
            yield "..."

        yield "_" * DASHBOARD_WIDTH

    def add_persisted_message(self, msg: str):
        self.persisted_messages.append(msg)

    def yield_dashboard_body_lines(self):
        """
        Iterates over self.data and yields
        text strings to be output. No Text
        formatting or alignment here.
        """
        if self.data:
            yield self.data["url"]
            yield "_" * DASHBOARD_WIDTH
            yield "Timeframe (in minutes): {}".format(
                self.secToMin(self.data["timeframe"])
            )
            yield "Report time: " + self.data["timestamp"]
            yield "_" * DASHBOARD_WIDTH
            for k, v in self.data.items():
                # Here I skip certain keys
                if k not in ["url", "timestamp", "timeframe"]:

                    if v is None:
                        # If there is no value yet
                        yield f"{k} -> Please wait"
                    # Custom % formatting for availability
                    elif k == "availability":
                        yield f"{k} -> " + "{0:.0%}".format(v)

                    # Basic text format
                    else:
                        yield f"{k} -> {v}"


class ConsoleWriter:
    """
    ConsoleWriter manages the writing to the console
    of multiple dashboards. It enforces text formatting.
    """

    def __init__(self):
        self.BOLD_LINE = "=" * 50
        self.SINGLE_LINE = "-" * 50
        self.WELCOME_MSG = "Website monitoring application"
        self.GOODBYE_MSG = "Come back soon!"
        self.APPLICATION_TITLE = "Web Monitoring Application"
        self.web_performance_dashboards = []

    def add_dashboard(self, wp_dashboard: WebPerformanceDashboard):
        self.web_performance_dashboards.append(wp_dashboard)

    def clear_screen(self):
        """
        Clears the console screen.
        """
        os.system("cls -y")

    def greet(self):
        """
        Application intro
        """
        self.clear_screen()
        greeting = f"{self.BOLD_LINE}\n{self.WELCOME_MSG}\n{self.SINGLE_LINE}"
        print(greeting)

    def goodbye(self):
        """
        Application outro
        """
        print(f"{self.SINGLE_LINE}\n{self.GOODBYE_MSG}\n{self.BOLD_LINE}")

    def yield_application_header_lines(self):
        """
        Yields console text strings one by one
        while represent single or multiple dashboards
        text representation. 
        """
        # The lenght of a header covering all dashboards
        multi_dashboard_length = len(self.web_performance_dashboards) * DASHBOARD_WIDTH

        yield "=" * multi_dashboard_length

        yield self.format_line(
            self.APPLICATION_TITLE,
            close_lines=True,
            pad_lines=True,
            max_length=multi_dashboard_length,
        )

        yield "=" * multi_dashboard_length

    def write_dashboards_to_console(self):
        """
        Yields console text strings one by one
        while represent single or multiple dashboards
        text representation. 
        """

        # Clear screen before outputting
        self.clear_screen()

        # Print the multi dashboard header
        for header_line in self.yield_application_header_lines():
            print(header_line)

        # Print dashboard bodies
        for dashboard_body_line in self.yield_dashboard_body_lines():
            print(dashboard_body_line)

        # Print alert history
        for alert in self.yield_alert_history_lines():
            print(alert)

        # Avoid blinking cursor on the output
        print("\n")

    def yield_alert_history_lines(self):
        """
        Yields console text strings one by one
        while represent single or multiple dashboards
        text representation. 

        History of alerts yielded here.
        """

        #  Concatenate the lienes from each dashboard
        # and format before printing multi dashboard line
        dashboard_persisted_msg_generators = [
            db.yield_persisted_messages() for db in self.web_performance_dashboards
        ]

        for line_items in zip(*dashboard_persisted_msg_generators):
            multi_db_body_line = ""
            for line in line_items:
                multi_db_body_line += self.format_line(
                    line, close_lines=True, pad_lines=True
                )

            yield multi_db_body_line

    def yield_dashboard_body_lines(self):
        """
        Yields console text strings one by one
        while represent single or multiple dashboards
        text representation. 

        Main body lines yielded here.
        """

        #  Concatenate the lienes from each dashboard
        # and format before printing multi dashboard line
        dashboard_body_generators = [
            db.yield_dashboard_body_lines() for db in self.web_performance_dashboards
        ]

        for line_items in zip(*dashboard_body_generators):

            multi_db_body_line = ""
            for line in line_items:
                multi_db_body_line += self.format_line(
                    line, close_lines=True, pad_lines=True
                )

            yield multi_db_body_line

    def truncate_lines(self, text_string, max_length):
        """
        Cuts strings to fit the max length and adds a ...
        at the end.
        """

        # Single char lines don't need final elipsis
        char_set = set(text_string)
        if len(char_set) == 1:
            result = text_string[:max_length]

        else:
            result = text_string[: max_length - 3] + "..."

        return result

    def pad_lines(self, text_string, max_len):
        """
        Adds spaces at start and end of string
        to force max length
        """
        line_length = len(text_string)

        pre_padding = int((max_len - line_length) / 2) * " "

        post_padding = (max_len - (line_length + len(pre_padding))) * " "

        text_string = pre_padding + text_string + post_padding

        return text_string

    def format_line(
        self,
        text_string: str,
        close_lines: bool,
        pad_lines: bool,
        max_length=DASHBOARD_WIDTH,
    ) -> str:
        """
        Takes a text input and formats it. Used to build
        multi dashboard outputs.

        PARAMETERS: text_string, the line to be written as
                    part of the dashboard
                    close_lines: bool. Should string include
                    | characters at either end
                    pad_lines: bool, should lines match the width
                    of the DASHBOARD constant
        """

        # Keep 2 chars for the closing characters
        max_length = max_length - 2 if close_lines else max_length

        # Truncate if necessary
        if max_length <= len(text_string):
            text_string = self.truncate_lines(text_string, max_length)

        if pad_lines:
            text_string = self.pad_lines(text_string, max_length)

        if close_lines:
            text_string = "|" + text_string + "|"

        return text_string
