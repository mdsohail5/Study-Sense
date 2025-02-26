import React, { useState, useEffect } from 'react';
import API from './Api';
import { useNavigate } from 'react-router-dom';
import './StudyData.css';

const StudyData = () => {
    const [studyData, setStudyData] = useState([]);
    const [studyTopic, setStudyTopic] = useState('');
    const [studyHours, setStudyHours] = useState('');
    const [studyDate, setStudyDate] = useState('');
    const [difficultyLevel, setDifficultyLevel] = useState('');
    const [subject, setSubject] = useState('');
    const [predictedMarks, setPredictedMarks] = useState(null);

    const navigate = useNavigate();

    useEffect(() => {
        fetchStudyData();
    }, []);

    const fetchStudyData = async () => {
        try {
            const res = await API.get('/study-data/');
            console.log("Fetched Study Data:", res.data);
            setStudyData(res.data);
        } catch (err) {
            console.error("Fetch Error:", err.response?.data || err.message);
        }
    };

    const addStudyData = async () => {
        if (!studyTopic || !studyHours || !studyDate || !difficultyLevel) {
            alert("All fields are required");
            return;
        }

        const newStudyData = { 
            study_topic: studyTopic, 
            study_hours: Number(studyHours), 
            study_date: studyDate, 
            difficulty_level: difficultyLevel 
        };

        try {
            await API.post('/study-data/', newStudyData);
            console.log("Added Study Data:", newStudyData);
            fetchStudyData();
            setStudyTopic('');
            setStudyHours('');
            setStudyDate('');
            setDifficultyLevel('');
        } catch (err) {
            console.error("Add Error:", err.response?.data || err.message);
        }
    };

    const fetchPredictedMarks = async () => {
        if (!subject || !studyHours) {
            alert("Subject and study hours are required");
            return;
        }

        try {
            const res = await API.get(`/predict-marks/?subject=${subject}&study_hours=${Number(studyHours)}`);
            console.log("Predicted Marks API Response:", res.data);

            if (res.data && res.data.predicted_marks !== undefined) {
                setPredictedMarks(res.data.predicted_marks);
            } else {
                console.error("Unexpected response format:", res.data);
                setPredictedMarks("Error fetching data");
            }
        } catch (err) {
            console.error("Prediction Error:", err.response?.data || err.message);
            setPredictedMarks("Failed to fetch");
        }
    };

    return (
        <div>
            <h1>Study Data Page</h1>

            {/* Study Records Section */}
            <div>
                <h2>Study Records</h2>
                <ul>
                    {studyData.map((study) => (
                        <li key={study.id}>
                            {study.study_hours} hours - {study.study_topic} - {study.study_date} - {study.difficulty_level}
                        </li>
                    ))}
                </ul>
            </div>

            {/* Add Study Data Section */}
            <div>
                <h2>Add Study Data</h2>
                <input type="text" placeholder="Study Topic" value={studyTopic} onChange={(e) => setStudyTopic(e.target.value)} />
                <input type="number" placeholder="Study Hours" value={studyHours} onChange={(e) => setStudyHours(e.target.value)} />
                <input type="date" placeholder="Study Date" value={studyDate} onChange={(e) => setStudyDate(e.target.value)} />
                <input type="text" placeholder="Difficulty Level" value={difficultyLevel} onChange={(e) => setDifficultyLevel(e.target.value)} />
                <button onClick={addStudyData}>Add Study Data</button>
            </div>

            {/* Predict Study Hours Section */}
            <div>
                <h2>Predict Marks Based on Study Hours</h2>
                <input type="text" placeholder="Subject" value={subject} onChange={(e) => setSubject(e.target.value)} />
                <input type="number" placeholder="Study Hours" value={studyHours} onChange={(e) => setStudyHours(e.target.value)} />
                <button onClick={fetchPredictedMarks}>Predict Marks</button>
                {predictedMarks !== null && (
                    <p>Predicted Marks: {typeof predictedMarks === "number" ? predictedMarks : JSON.stringify(predictedMarks)}</p>
                )}
            </div>
        </div>
    );
};

export default StudyData;
