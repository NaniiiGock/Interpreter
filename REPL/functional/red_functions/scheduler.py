from subprocess import Popen, PIPE
from ..BaseClassFunction import RedFunction


class ScheduleCommand(RedFunction):
    @staticmethod
    def get_confirmation_message(frequency: str, command: str):
        return f"Confirm scheduling command: {command} with the frequency: {frequency}."

    @staticmethod
    def run(frequency: str, command: str):
        """
        schedule_command
        :param frequency: frequency for command to run
        :param command: command to schedule
        :return:
        """
        cron_command = f"(crontab -l ; echo '{frequency} {command}') | crontab -"
        p = Popen(cron_command, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE, universal_newlines=True)
        return p.returncode, None, None


class RemoveScheduledCommand(RedFunction):
    @staticmethod
    def get_confirmation_message(frequency: str, command: str):
        return f"Confirm removing scheduled command: {command} with frequency: {frequency}."

    @staticmethod
    def run(frequency: str, command: str):
        # Get the current crontab
        p = Popen("crontab -l", shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE, universal_newlines=True)
        current_crontab, _ = p.communicate()

        # Remove the specified command from the crontab
        lines = current_crontab.split('\n')
        new_crontab = '\n'.join([line for line in lines if f"{frequency} {command}" not in line])

        # Apply the updated crontab
        p = Popen("crontab -", shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE, universal_newlines=True)
        p.communicate(input=new_crontab)
        return p.returncode, None, None
