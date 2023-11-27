//
// Created by Anastasiaa on 27.11.2023.
//

#ifndef LOCAL_INTERPRETER_TASKSCHEDULER_H
#define LOCAL_INTERPRETER_TASKSCHEDULER_H

#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <algorithm>


class TaskScheduler {
private:
    std::vector<std::string> cronJobs;

    void updateCrontab();

public:
    TaskScheduler() = default;

    void add_cron_job(const std::string& cronJob);

    void remove_cron_job(const std::string& cronJob);

    void remove_all_jobs();

    void list_cron_jobs();
};



#endif //LOCAL_INTERPRETER_TASKSCHEDULER_H
