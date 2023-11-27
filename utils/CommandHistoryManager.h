//
// Created by Anastasiaa on 25.11.2023.
//

#ifndef LOCAL_INTERPRETER_COMMANDHISTORYMANAGER_H
#define LOCAL_INTERPRETER_COMMANDHISTORYMANAGER_H

#include <string>


class CommandHistoryManager {
private:
    std::string exeDir;
    std::string history_file_path;
public:
    explicit CommandHistoryManager(const std::string& exe_dir);

    void read_history_commands();

    void add_to_history_commands(const std::string& command);

    void write_history_commands();
};


#endif //LOCAL_INTERPRETER_COMMANDHISTORYMANAGER_H
