# TASKING 
Command-line Task Manager for user registration, task management, and user session tracking

<div align="center">
   <img src="https://github.com/Daniel-Alvarenga/Tasking/assets/128755697/a7a773a0-59b3-4fee-9648-ff5b1d966fea"/>
</div>

The **Tasking** is a command-line Python project designed for user account management and task tracking. It provides functionalities for user registration, secure password hashing, login sessions, and task management. Users can create, view, mark as completed, and delete tasks associated with their account. This project stores user data, task details, and login history in a JSON file for persistence.

### Features:
- User registration with hashed password storage.
- User login with password verification.
- Create, view, mark as completed, and delete tasks.
- Session management with a one-hour timeout.
- Recording of user login sessions and timestamps.
- Command-line interface (CLI) for user interaction.
- Data persistence in a JSON file.

This Task Manager is a simple yet functional tool for efficient task management and record-keeping.

### Getting Started:
1. Clone this repository.
2. Run the `task_manager.py` script to use the Task Manager via the command line.

### Usage:
- `login`: Log in with your username and password.
- `register`: Register a new user with a username and password.
- `new`: Create a new task.
- `view`: View your tasks.
- `remove`: Delete a task.
- `conclude`: Mark a task as completed.
- `getdata`: Display user login data.
- `help`: View available commands.

## How to Use

Follow these steps to get started with the Task Manager on your local machine.

### Prerequisites

- Python 3.x installed on your machine. You can download it from [python.org](https://www.python.org/downloads/).

### Clone the Repository

1. Open your terminal or command prompt.

2. Clone the repository to your computer using the command:

   ```bash
     git clone https://github.com/your-username/task-manager.git
   ```
3. Navigate to the project directory:
    ```bash
      cd Tasking
    ```

4. Run the Project
    Run the task_manager.py script to start using the Task Manager:
    ```bash
        python __main__.py
    ```

The project will respond with a command prompt, and you can begin using the Task Manager's features.

**Note for Windows Users (PowerShell):**

If you're using PowerShell on Windows, you can create a custom function for executing the Task Manager more conveniently. Here's how you can do it:

1. Open PowerShell.

2. Run the following command to create a custom function:

    ```powershell
       function Tasking {
           python "path\to\Tasking\__main__.py" $args
      }
    ```

Replace `"path\to\Tasking\__main__.py"` with the actual path to your `__main__.py` file.

3. Once the function is created, you can use it to execute the Task Manager with a simplified command. For example, to run a command like `tasking option`, you can simply type:

    ```powershell
    tasking option
    ```
This custom function makes it more convenient to run the Task Manager from PowerShell on Windows.
