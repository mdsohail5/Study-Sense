import React, { useState, useEffect } from 'react';
import API from './Api';
import { useNavigate } from 'react-router-dom';
import './ExamMarks.css';

const ExamMarks = () => {
    const [examMarksData, setExamMarksData] = useState([]);
    const [subject, setSubject] = useState('');
    const [examDate, setExamDate] = useState('');
    const [preparationStartDate, setPreparationStartDate] = useState('');
    const [hoursStudied, setHoursStudied] = useState('');
    const [marksObtained, setMarksObtained] = useState('');
    const [totalMarks, setTotalMarks] = useState('');
    const [desiredMarks, setDesiredMarks] = useState('');
    const [requiredStudyHours, setRequiredStudyHours] = useState(null);
    const navigate = useNavigate();

    useEffect(() => {
        fetchExamMarks();
    }, []);

    const fetchExamMarks = async () => {
        try {
            const res = await API.get('/exam-marks/');
            console.log("Fetched Data:", res.data);
            setExamMarksData(res.data);
        } catch (err) {
            console.error("Fetch Error:", err.response?.data || err.message);
        }
    };

    const addExamMark = async () => {
        if (!subject || !examDate || !preparationStartDate || !hoursStudied || !marksObtained || !totalMarks) {
            alert("All fields are required");
            return;
        }

        const newExamMark = { 
            subject, 
            exam_date: examDate, 
            preparation_start_date: preparationStartDate, 
            hours_studied: Number(hoursStudied), 
            marks_obtained: Number(marksObtained), 
            total_marks: Number(totalMarks) 
        };

        try {
            const res = await API.post('/exam-marks/', newExamMark);
            console.log("Added Data:", res.data);
            fetchExamMarks();
            setSubject('');
            setExamDate('');
            setPreparationStartDate('');
            setHoursStudied('');
            setMarksObtained('');
            setTotalMarks('');
        } catch (err) {
            console.error("Add Error:", err.response?.data || err.message);
        }
    };

    const removeExamMark = async (id) => {
        try {
            await API.delete(`/exam-marks/${id}/`);
            console.log(`Deleted Record ID: ${id}`);
            fetchExamMarks();
        } catch (err) {
            console.error("Delete Error:", err.response?.data || err.message);
        }
    };

    const fetchRequiredStudyHours = async () => {
        if (!subject || !desiredMarks) {
            alert("Subject and desired marks are required");
            return;
        }

        try {
            const res = await API.get(`/required-study-hours/?subject=${subject}&desired_marks=${Number(desiredMarks)}`);
            console.log("API Response:", res.data); // Debugging
            if (res.data && res.data.required_study_hours !== undefined) {
                setRequiredStudyHours(res.data.required_study_hours);
            } else {
                console.error("Invalid response format:", res.data);
                setRequiredStudyHours("Error fetching data");
            }
        } catch (err) {
            console.error("Prediction Error:", err.response?.data || err.message);
            setRequiredStudyHours("Failed to fetch");
        }
    };

    return (
        <div>
            <h1>Exam Marks Page</h1>

            {/* Exam Records Section */}
            <div>
                <h2>Exam Marks Records</h2>
                <ul>
                    {examMarksData.map((examMark) => (
                        <li key={examMark.id}>
                            {examMark.subject} - {examMark.exam_date} - {examMark.preparation_start_date} - 
                            {examMark.hours_studied} hours - {examMark.marks_obtained}/{examMark.total_marks} marks
                            <button onClick={() => removeExamMark(examMark.id)}>Remove</button>
                        </li>
                    ))}
                </ul>
            </div>

            {/* Add Exam Marks Section */}
            <div>
                <h2>Add Exam Marks</h2>
                <input type="text" placeholder="Subject" value={subject} onChange={(e) => setSubject(e.target.value)} />
                <input type="date" value={examDate} onChange={(e) => setExamDate(e.target.value)} />
                <input type="date" value={preparationStartDate} onChange={(e) => setPreparationStartDate(e.target.value)} />
                <input type="number" placeholder="Hours Studied" value={hoursStudied} onChange={(e) => setHoursStudied(e.target.value)} />
                <input type="number" placeholder="Marks Obtained" value={marksObtained} onChange={(e) => setMarksObtained(e.target.value)} />
                <input type="number" placeholder="Total Marks" value={totalMarks} onChange={(e) => setTotalMarks(e.target.value)} />
                <button onClick={addExamMark}>Add Exam Data</button>
            </div>

            {/* Predict Study Hours Section */}
            <div>
                <h2>Predict Required Study Hours</h2>
                <input type="text" placeholder="Subject" value={subject} onChange={(e) => setSubject(e.target.value)} />
                <input type="number" placeholder="Desired Marks" value={desiredMarks} onChange={(e) => setDesiredMarks(e.target.value)} />
                <button onClick={fetchRequiredStudyHours}>Predict Study Hours</button>
                {requiredStudyHours !== null && (
                    <p>Required Study Hours: { requiredStudyHours === "number" ? requiredStudyHours : JSON.stringify(requiredStudyHours)}</p>
                )}
            </div>
        </div>
    );
};

export default ExamMarks;
