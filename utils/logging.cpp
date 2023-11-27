//
// Created by Anastasiaa on 25.11.2023.
//

#include <cstdlib>
#include <mach-o/dyld.h>

#include <filesystem>

#include "logging.h"


std::string getExecutablePath() {
    char path[PATH_MAX];
    uint32_t size = sizeof(path);
    // file system path of the executable of the current process
    // from macOS Application Services framework
    if (_NSGetExecutablePath(path, &size) != 0) {
        // Buffer size is too small.
        return "";
    }
    return {path};
}

std::string getDirectoryFromPath(const std::string& path) {
    size_t found = path.find_last_of("/\\");
    return path.substr(0, found);
}

void show_logo(const std::string& exeDir) {
    std::string print_logo_script = "/../utils/logo.sh";
    std::string command = "bash " + exeDir + print_logo_script;
    system(command.c_str());
}

std::string get_start_of_the_line() {
    std::string prompt_path = std::filesystem::current_path().string();
    prompt_path = contract_tilde(prompt_path);
    return prompt_path + " $ ";
}

std::string contract_tilde(const std::string &path) {
    static const std::string home_dir = getenv("HOME") ? getenv("HOME") : "";
    if (home_dir.empty()) {
        return path;  // If HOME is not set, return the original path
    }

    if (path.compare(0, home_dir.length(), home_dir) == 0) {
        // Replace the home directory with ~
        return "~" + path.substr(home_dir.length());
    }
    return path;
}