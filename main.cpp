
#include "logging.h"
#include "ErrorCodes.h"
#include "CommandHistoryManager.h"
#include "pipeline_execution.h"
#include "TaskScheduler.h"


int main() {
    std::string exePath = getExecutablePath();
    std::string exeDir = getDirectoryFromPath(exePath);

    show_logo(exeDir);

    CommandHistoryManager historyManager(exeDir);
    historyManager.read_history_commands();

    TaskScheduler task_scheduler;

    // pipeline execution
    int error_code = execute_pipeline(historyManager, task_scheduler);
    if (error_code != ErrorCodes::CODE_OK) return error_code;

    historyManager.write_history_commands();

    return ErrorCodes::CODE_OK;
}
