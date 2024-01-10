from subprocess import Popen, PIPE
from REPL.functional.BaseClassFunction import RedFunction
import asyncio


class ScheduleCommand(RedFunction):
    @staticmethod
    def get_exec_description():
        return "Scheduling command..."

    @staticmethod
    async def run_async(frequency: str, command: str):
        cron_command = f"(crontab -l ; echo '{frequency} {command}') | crontab -"
        return await asyncio.get_event_loop().run_in_executor(
            None, run_sched_command, cron_command
        )

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

        return {
            'returncode': p.returncode,
            'stdout': None,
            'stderr': None
        }


def run_sched_command(cron_command: str):
    p = Popen(cron_command, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE, universal_newlines=True)
    stdout, stderr = p.communicate()
    return p.returncode, stdout, stderr


def run_remove_sched_command(cron_command: str, input_data=None):
    p = Popen(cron_command, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE, universal_newlines=True)
    stdout, stderr = p.communicate(input=input_data)
    return p.returncode, stdout, stderr


class RemoveScheduledCommand(RedFunction):
    @staticmethod
    def get_exec_description():
        return "Removing scheduled command..."

    @staticmethod
    async def run_async(frequency: str, command: str):
        get_cron_command = "crontab -l"
        remove_cron_command = "crontab -"

        current_crontab, stdout, stderr = await asyncio.get_event_loop().run_in_executor(
            None, run_remove_sched_command, get_cron_command
        )

        # removing all quotes before matching
        stdout = stdout.replace("'", "").replace('"', '')
        command = command.replace("'", "").replace('"', '')

        lines = stdout.split('\n')
        new_crontab = '\n'.join([line for line in lines if f"{frequency} {command}" not in line])

        return await asyncio.get_event_loop().run_in_executor(
            None, run_remove_sched_command, remove_cron_command, new_crontab
        )

    @staticmethod
    def get_confirmation_message(frequency: str, command: str):
        return f"Confirm removing scheduled command: {command} with frequency: {frequency}."

    @staticmethod
    def run(frequency: str, command: str):
        # Get the current crontab
        p = Popen("crontab -l", shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE, universal_newlines=True)
        current_crontab, _ = p.communicate()

        # removing all quotes before matching
        current_crontab = current_crontab.replace("'", "").replace('"', '')
        command = command.replace("'", "").replace('"', '')

        # Remove the specified command from the crontab
        lines = current_crontab.split('\n')
        new_crontab = '\n'.join([line for line in lines if f"{frequency} {command}" not in line])

        # Apply the updated crontab
        p = Popen("crontab -", shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE, universal_newlines=True)
        p.communicate(input=new_crontab)
        return {
            'returncode': p.returncode,
            'stdout': None,
            'stderr': None
        }

async def main():
    # Start the run_async task but don't wait here
    task = asyncio.create_task(RemoveScheduledCommand.run_async("* * * * *", "echo 'hello' > /tmp/hello.txt"))

    # Do some other stuff while run_async is running
    print("Doing other things while scheduling...")
    await asyncio.sleep(2)  # Simulate some other work
    print("main")

    result = await task
    # Now, wait for the run_async task to complete if it hasn't already
    print(result)


if __name__ == '__main__':
    asyncio.run(main())
    # RemoveScheduledCommand.run("* * * * *", "echo 'hello' > /tmp/hello.txt")