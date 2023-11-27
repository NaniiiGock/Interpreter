//
// Created by Anastasiaa on 27.11.2023.
//

#include "TaskScheduler.h"


void TaskScheduler::updateCrontab() {
    std::ofstream tempCrontabWrite("temp_crontab");
    for (const auto& job : cronJobs) {
        tempCrontabWrite << job << std::endl;
    }
    tempCrontabWrite.close();
    system("crontab temp_crontab");
    system("rm temp_crontab");
}


void TaskScheduler::add_cron_job(const std::string &cronJob) {
    cronJobs.push_back(cronJob);
    updateCrontab();
    std::cout << "Cron job added: " << cronJob << std::endl;
}


void TaskScheduler::remove_cron_job(const std::string &cronJob) {
    auto it = std::find(cronJobs.begin(), cronJobs.end(), cronJob);
    if (it != cronJobs.end()) {
        cronJobs.erase(it);
        updateCrontab();
        std::cout << "Cron job removed: " << cronJob << std::endl;
    } else {
        std::cout << "Cron job not found: " << cronJob << std::endl;
    }
}


void TaskScheduler::list_cron_jobs() {
    std::cout << "Current Cron Jobs:" << std::endl;
    for (const auto& job : cronJobs) {
        std::cout << job << std::endl;
    }
}

void TaskScheduler::remove_all_jobs() {
    cronJobs.clear();
    updateCrontab();
    std::cout << "All cron jobs removed." << std::endl;
}
