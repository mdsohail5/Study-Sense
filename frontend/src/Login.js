import React , {useState} from 'react';
import { useNavigate } from 'react-router-dom';
import API from './Api'

const Login = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('')
    const [error, setError] = useState('')
    const naviagte = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        try{
            const response = await API.post('/token/',{ username, password });
            localStorage.setItem('token',response.data.access);
            naviagte('/');
        } catch(err){
            setError('Invalid username or password')
        }
    };
    
    return (
        <div>
            <form onSubmit={handleSubmit} >
            <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
          <button type="submit">Log In</button>

            </form>
            { error && <p style={{color :'red'}}>{error}</p> }
            <p>
                Don't have an account? <a href="/register">Sign up</a>
            </p>
        </div>
    );
};

export default Login;