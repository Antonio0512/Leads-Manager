import {useContext} from "react";

import {UserContext} from "../context/UserContext";
import {Navigate, Outlet} from "react-router-dom";

export const AuthRouteGuard = ({children}) => {
    const {isAuthenticated} = useContext(UserContext);

    if (!isAuthenticated) {
        return <Navigate to="/login"/>;
    }

    return children ? children : <Outlet/>;
};