//
// Created by Anastasiaa on 28.11.2023.
//

#include <iostream>
#include <sstream>
#include <memory>
#include <stdexcept>


std::string executeCommand(const std::string& cmd) {
    std::unique_ptr<FILE, decltype(&pclose)> pipe(popen(cmd.c_str(), "r"), pclose);
    if (!pipe) throw std::runtime_error("popen() failed!");

    std::ostringstream resultStream;
    char buffer[256];

    while (fgets(buffer, sizeof(buffer), pipe.get()) != nullptr) {
        resultStream << buffer;
    }

    return resultStream.str();
}


void modifyCronJobs(const std::string& command, bool remove = false) {
    std::string currentCrontab = executeCommand("crontab -l");

    std::istringstream iss(currentCrontab);
    std::string modifiedCrontab;
    std::string line;
    bool commandFound = false;

    while (std::getline(iss, line)) {
        if (line != command) {
            modifiedCrontab += line + "\n";
        } else {
            commandFound = true;
        }
    }

    if (remove) {
        if (!commandFound) {
            std::cerr << "Command not found in crontab.\n";
            return;
        }
    } else {
        if (commandFound) {
            std::cerr << "Command already exists in crontab.\n";
            return;
        }
        modifiedCrontab += command + "\n";
    }
    std::string updateCmd = "echo \"" + modifiedCrontab + "\" | crontab -";
    executeCommand(updateCmd);
}


int main(int argc, char* argv[]) {
    if (argc < 2) {
        std::cerr << "Usage: " << argv[0] << " [-rm] command\n";
        return 1;
    }
    std::string command = (argc == 3 && std::string(argv[1]) == "-rm") ? argv[2] : argv[1];
    modifyCronJobs(command, argc == 3 && std::string(argv[1]) == "-rm");
    return 0;
}
