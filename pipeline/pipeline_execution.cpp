//
// Created by Anastasiaa on 27.11.2023.
//
#include <iostream>
#include <readline/readline.h>

#include "pipeline_execution.h"

#include "model.h"
#include "logging.h"
#include "../ErrorCodes.h"


int execute_pipeline(CommandHistoryManager& historyManager, TaskScheduler& task_scheduler) {

    // TODO: now its predefined command to play song every minute -> needs to be rewritten after parsing model output
    // Play song every two minutes
    std::string temp_command = R"(*/2 * * * * osascript -e 'tell application "Music" to play track "You Drive My Four Wheel Coffin"')";

    while (true) {
        std::string start_of_line = get_start_of_the_line();
        char *buf = readline(start_of_line.c_str());

        if (!buf) {
            std::cout << std::endl;
            break;
        }

        if (buf[0] != 0) historyManager.add_to_history_commands(buf);

        std::string cmd_line(buf);
        free(buf);

        if (cmd_line == "exit") break;

        if (cmd_line == "add_sched_music") { // Temporary "if" to show TaskScheduler functionality
            task_scheduler.add_cron_job(temp_command);
        } else if (cmd_line == "rm_sched_music") { // Temporary "if" to show TaskScheduler functionality
            task_scheduler.remove_cron_job(temp_command);
        } else if (cmd_line == "list_sched") { // Temporary "if" to show TaskScheduler functionality
            task_scheduler.list_cron_jobs();
        } else {
            std::cout << "LLM answer: " << get_answer(cmd_line) << std::endl;
        }
    }
    return ErrorCodes::CODE_OK;
}