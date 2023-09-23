import {useContext} from "react";
import {UserContext} from "../context/UserContext";

export const Header = () => {
    const {user, setUser} = useContext(UserContext);

    const onLogout = () => {
        setUser({});
    };

    return (
        <div className="has-text-centered m-6">
            <h1 className="title">Welcome to the Leads Manager</h1>
            {user.access_token && (
                <button className="button" onClick={onLogout}>Logout</button>
            )}
        </div>
    )
};