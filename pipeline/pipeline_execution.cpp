//
// Created by Anastasiaa on 27.11.2023.
//
#include <iostream>
#include <readline/readline.h>

#include "pipeline_execution.h"

#include "model.h"
#include "logging.h"
#include "../ErrorCodes.h"


int execute_pipeline(CommandHistoryManager& historyManager) {
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
        std::cout << "LLM answer: " << get_answer(cmd_line) << std::endl;
    }
    return ErrorCodes::CODE_OK;
}