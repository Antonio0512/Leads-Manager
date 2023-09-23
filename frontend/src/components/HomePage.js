import {useContext} from "react";
import {UserContext} from "../context/UserContext";
import {Link} from "react-router-dom";

export const HomePage = () => {
    const {isAuthenticated} = useContext(UserContext);

    return (
        <div className="container">
            <section className="section">
                <div className="columns is-centered">
                    <div className="column is-half">
                        <div className="box">
                            {!isAuthenticated ? (
                                <div>
                                    <Link to="/register" className="button is-link">
                                        Register
                                    </Link>
                                    <Link to="/login" className="button is-link ml-6">
                                        Login
                                    </Link>
                                </div>
                            ) : (
                                <p>
                                    <Link to={"/leads"} className="button is-link">
                                        Leads
                                    </Link>
                                </p>
                            )}
                        </div>
                    </div>
                </div>
            </section>
        </div>
    );
};
