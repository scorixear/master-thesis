use std::{env, path::{Path, PathBuf}, fs::File, io::{BufReader, BufRead, Error, self, Write}, collections::HashMap};
use chrono;

struct LogEntry {
    jobid: String,
    partition: String,
    name: String,
    user: String,
    status: String,
    time: String,
    nodes: String,
    nodelist: String
}

fn read_lines(filename: &Path) -> Result<Vec<String>, Error> {
    let file = File::open(filename)?;
    let reader = BufReader::new(file);
    Ok({
        let this = reader.lines().into_iter();
        this.map(|line| line.unwrap()).collect()
    })
}

fn get_current_dir() -> io::Result<PathBuf> {
    let exe = env::current_exe()?;
    let dir = exe.parent().expect("Executable must be in a directory");
    let dir = dir.to_path_buf();
    Ok(dir.to_path_buf())
}

fn unwrap_argument(log_entry: &mut LogEntry, split: Option<&str>, arg: &str) -> Option<String> {
    if split.is_none() {
        return None;
    }

    let split = split.unwrap();
    if split.is_empty() {
        return None;
    }

    match arg {
        "JobId" => log_entry.jobid = split.to_string(),
        "Partition" => log_entry.partition = split.to_string(),
        "Name" => log_entry.name = split.to_string(),
        "User" => log_entry.user = split.to_string(),
        "State" => log_entry.status = split.to_string(),
        "Time" => log_entry.time = split.to_string(),
        "Nodes" => log_entry.nodes = split.to_string(),
        "NodeList" => log_entry.nodelist = split.to_string(),
        _ => return None
    }
    Some(split.to_string())
}

fn main() -> Result<(), Error> {
    let args: Vec<String> = env::args().collect();
    let current_dir = match get_current_dir() {
        Ok(dir) => dir,
        Err(_) => return Err(Error::new(io::ErrorKind::Other, "Could not get current directory"))
    };

    let mut input_file = current_dir.clone();
    input_file.push("log.txt");
    if args.len() >= 2 {
        input_file = Path::new(&args[1]).to_path_buf();
    }

    let lines = read_lines(input_file.as_path());
    if let Err(err) = lines {
        return Err(err);
    }

    let mut counter: HashMap<(String, String), u32> = HashMap::new();
    for line in lines.unwrap() {
        let mut entry = LogEntry {
            jobid: String::new(),
            partition: String::new(),
            name: String::new(),
            user: String::new(),
            status: String::new(),
            time: String::new(),
            nodes: String::new(),
            nodelist: String::new()
        };
        let mut split = line.split_whitespace();
        let mut unwrapped = unwrap_argument(&mut entry, split.next(), "JobId");
        if let None = unwrapped {
            continue;
        }
        unwrapped = unwrap_argument(&mut entry, split.next(), "Partition");
        if let None = unwrapped {
            continue;
        }
        unwrapped = unwrap_argument(&mut entry, split.next(), "Name");
        if let None = unwrapped {
            continue;
        }
        unwrapped = unwrap_argument(&mut entry, split.next(), "User");
        if let None = unwrapped {
            continue;
        }
        let user = unwrapped.unwrap();
        unwrapped = unwrap_argument(&mut entry, split.next(), "State");
        if let None = unwrapped {
            continue;
        }
        let state = unwrapped.unwrap();
        unwrapped = unwrap_argument(&mut entry, split.next(), "Time");
        if let None = unwrapped {
            continue;
        }
        unwrapped = unwrap_argument(&mut entry, split.next(), "Nodes");
        if let None = unwrapped {
            continue;
        }
        unwrapped = unwrap_argument(&mut entry, split.next(), "NodeList");
        if let None = unwrapped {
            continue;
        }
        if counter.contains_key(&(user.clone(), state.clone())) {
            let count = counter.get_mut(&(user, state)).unwrap();
            *count += 1;
        } else {
            counter.insert((user, state), 1);
        }
    }

    let mut pending: Vec<(String, u32)> = Vec::new();
    let mut running: Vec<(String, u32)> = Vec::new();
    for (key, value) in counter {
        if key.1 == "PD" {
            pending.push((key.0, value));
        } else if key.1 == "R" {
            running.push((key.0, value));
        }
    }
    pending.sort_by(|a, b| b.1.cmp(&a.1));
    running.sort_by(|a, b| b.1.cmp(&a.1));

    let mut output = "user,status,count\n".to_string();
    for (user, count) in pending {
        output.push_str(&format!("{},pending,{}\n", user, count));
    }
    for (user, count) in running {
        output.push_str(&format!("{},running,{}\n", user, count));
    }

    let mut output_file = current_dir.clone();
    let current_time = chrono::Local::now();
    let current_time = current_time.format("%Y-%m-%d_%H-%M").to_string();
    output_file.push(format!("{}.csv", current_time));
    let mut file = File::create(output_file.as_path())?;
    file.write_all(output.as_bytes())?;
    file.flush()?;
    Ok(())
}
