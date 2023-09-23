import {createContext} from "react";
import * as userService from '../services/userService'
import {useLocalStorage} from "../hooks/useLocalStorage";

export const UserContext = createContext(undefined);

export const UserProvider = ({children}) => {
    const [user, setUser] = useLocalStorage("auth", {});

    const signUp = async (credentials) => {
        try {
            const userData = await userService.signUp(credentials);
            setUser(userData);
        } catch (error) {
            throw error
        }
    };


    const signIn = async (credentials) => {
        try {
            const userData = await userService.singIn(credentials);
            setUser(userData);
        } catch (error) {
            throw error
        }
    };

    const userContextData = {
        user,
        setUser,
        isAuthenticated: user?.access_token,
        signUp,
        signIn
    };

    return (
        <UserContext.Provider value={userContextData}>
            {children}
        </UserContext.Provider>
    )
};
