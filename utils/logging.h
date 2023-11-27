//
// Created by Anastasiaa on 25.11.2023.
//

#ifndef LOCAL_INTERPRETER_LOGGING_H
#define LOCAL_INTERPRETER_LOGGING_H

#include <iostream>

std::string getExecutablePath();
std::string getDirectoryFromPath(const std::string& path);

void show_logo(const std::string& exeDir);

std::string get_start_of_the_line();
std::string contract_tilde(const std::string &path);

#endif //LOCAL_INTERPRETER_LOGGING_H
