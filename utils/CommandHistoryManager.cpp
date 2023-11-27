//
// Created by Anastasiaa on 25.11.2023.
//
#include <readline/readline.h>
#include "CommandHistoryManager.h"


CommandHistoryManager::CommandHistoryManager(const std::string& exe_dir) {
    std::string relative_history_file_path = "/../data/commands_history.txt";
    exeDir = exe_dir;
    history_file_path = exeDir + relative_history_file_path;
}

void CommandHistoryManager::read_history_commands() {
    read_history(history_file_path.c_str());
}

void CommandHistoryManager::add_to_history_commands(const std::string& command) {
    add_history(command.c_str());
}

void CommandHistoryManager::write_history_commands() {
    write_history(history_file_path.c_str());
}