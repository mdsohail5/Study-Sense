import React, { useState, useEffect } from 'react';
import API from './Api';
import { useNavigate } from 'react-router-dom';

const HomePage = () => {
    const [tasks, setTasks] = useState([]);
    const [title, setTitle] = useState('');
    const [description, setDescription] = useState('');
    const [completed, setCompleted] = useState(false);
    const navigate = useNavigate();

    useEffect(() => {
        fetchTasks();
    }, []);

    const fetchTasks = () => {
        API.get('/tasks/')
            .then((res) => setTasks(res.data))
            .catch((err) => console.log(err));
    };

    const addTask = () => {
        if (!title || !description) return alert("Title and Description are required");

        const newTask = { title, description, completed };
        API.post('/tasks/', newTask)
            .then(() => {
                fetchTasks();
                setTitle('');
                setDescription('');
                setCompleted(false);
            })
            .catch((err) => console.log(err));
    };

    const deleteTask = (id) => {
        API.delete(`/tasks/${id}/`)
            .then(() => fetchTasks())
            .catch((err) => console.log(err));
    };

    const goToAddStudyData = ()=> {
        navigate('/studyhours')
    };

    const goToAddExamMarks = ()=> {
        navigate('/ExamMarks')
    }

    const goToPredictions = ()=>{
        navigate('/predictions')
    }
    return (
        <div>
            <h1>Task Manager</h1>
            <div>
                <h2>Add a New Task</h2>
                <input
                    type="text"
                    placeholder="Title"
                    value={title}
                    onChange={(e) => setTitle(e.target.value)}
                />
                <input
                    type="text"
                    placeholder="Description"
                    value={description}
                    onChange={(e) => setDescription(e.target.value)}
                />
                <button onClick={addTask}>Add Task</button>
            </div>

            <div>
                <h2>Here are tasks</h2>
                <ul>
                    {tasks.map((task) => (
                        <li key={task.id}>
                            <strong>{task.title}</strong>: {task.description} - {task.completed ? 'Completed' : 'Pending'}
                            <button onClick={() => deleteTask(task.id)}>Delete</button>
                        </li>
                    ))}
                </ul>
            </div>
            <div>
                <button onClick={goToAddStudyData}>Add Study Data</button>
                <button onClick={goToAddExamMarks}>Add Exam Marks</button>
                <button onClick={goToPredictions}>Predict Marks</button>
            </div>
        </div>
    );
};

export default HomePage;
