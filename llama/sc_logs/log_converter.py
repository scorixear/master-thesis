import sys
import os
import re

from datetime import datetime


class Job:
    def __init__(self, line) -> None:
        match = re.match(
            "^ *([^ ]+) *([^ ]+) *([^ ]+) *([^ ]+) *([^ ]+) *([^ ]+) *([^ ]+) *([^ ]+)$",
            line,
        )
        assert match is not None

        self.jobid: str = match.group(1)
        self.partition: str = match.group(2)
        self.name: str = match.group(3)
        self.user: str = match.group(4)
        self.status: str = match.group(5)
        self.time: str = match.group(6)
        self.nodes: str = match.group(7)
        self.nodelist: str = match.group(8)

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, Job):
            return self.jobid == __value.jobid
        return False

    def __hash__(self) -> int:
        return hash(self.jobid)

    def __str__(self) -> str:
        return f"{self.jobid}: {self.user} - {self.status}"

    def __repr__(self) -> str:
        return str(self)

    def check_user(self, other: "Job") -> bool:
        return self != other and self.user == other.user and self.status == other.status


def main():
    if(len(sys.argv) < 2):
        input_file = os.path.dirname(__file__)+"/log.txt"
    else:
        input_file = sys.argv[1]
    with open(input_file, "r", encoding="UTF-8") as file:
        logs = file.read()

    lines = logs.splitlines()[1:]
    job_count: dict[tuple[str, str], int] = {}
    jobs = []
    for line in lines:
        if(line.strip() == ""):
            continue
        try:
            job = Job(line)
            jobs.append(job)
            if (job.user, job.status) not in job_count:
                job_count[(job.user, job.status)] = 1
            else:
                job_count[(job.user, job.status)] += 1
        except:
            continue
    converted = [(value[0], value[1], count) for value, count in job_count.items()]
    pending = [(value[0], value[2]) for value in converted if value[1] == "PD"]
    pending.sort(key=lambda x: x[1], reverse=True)
    running = [(value[0], value[2]) for value in converted if value[1] == "R"]
    running.sort(key=lambda x: x[1], reverse=True)
    output = "user,status,count\n"
    output += "\n".join([f"{value[0]},PD,{value[1]}" for value in pending])+"\n"
    output += "\n".join([f"{value[0]},R,{value[1]}" for value in running])
    with open(
        os.path.dirname(__file__)+"/"+ datetime.now().strftime("%Y-%m-%d_%H_%M") + ".csv", "w", encoding="UTF-8"
    ) as file:
        file.write(output)


if __name__ == "__main__":
    main()
