import {UserContext} from "../context/UserContext";
import {useContext, useState} from "react";
import {useNavigate} from "react-router-dom";
import {ErrorMessage} from "./ErrorMessages";

export const SignUp = () => {
    const navigate = useNavigate();

    const {signUp} = useContext(UserContext)

    const [error, setError] = useState("");
    const [formData, setFormData] = useState({
        email: "",
        password: "",
        confirm_password: ""
    });

    const {email, password, confirm_password} = formData;

    const onChange = (e) => setFormData({...formData, [e.target.name]: e.target.value});

    const onSubmit = async (e) => {
        e.preventDefault();

        try {
            await signUp({email, password, confirm_password});
            navigate("/");
        } catch (error) {
            setError(error.response.data.detail);
        }
    };


    return (
        <div className="column">
            <form className="box" onSubmit={e => onSubmit(e)}>
                <h1 className="title has-text-centered">Register</h1>
                <div className="field">
                    <label className="label" htmlFor="email">Email Address</label>
                    <div className="control">
                        <input
                            className="input"
                            type="email"
                            placeholder="Enter email"
                            name="email"
                            id="email"
                            value={email}
                            onChange={e => onChange(e)}
                            required
                            autoComplete="email"
                        />
                    </div>
                </div>
                <div className="field">
                    <label className="label" htmlFor="password">Password</label>
                    <div className="control">
                        <input
                            className="input"
                            type="password"
                            placeholder="Enter password"
                            name="password"
                            id="password"
                            value={password}
                            onChange={e => onChange(e)}
                            required
                            autoComplete="new-password"
                        />
                    </div>
                </div>
                <div className="field">
                    <label className="label" htmlFor="confirm_password">Confirm Password</label>
                    <div className="control">
                        <input
                            className="input"
                            type="password"
                            placeholder="Enter password again"
                            name="confirm_password"
                            id="confirm_password"
                            value={confirm_password}
                            onChange={e => onChange(e)}
                            required
                            autoComplete="new-password"
                        />
                    </div>
                </div>

                <ErrorMessage message={error}/>
                <br/>
                <button className="button is-primary" type="submit">Register</button>
            </form>
        </div>
    );
};