import {UserProvider} from "./context/UserContext";
import {Route, Routes} from "react-router-dom";
import {SignUp} from "./components/SignUp";
import {Header} from "./components/Header";
import {SignIn} from "./components/SignIn";

const App = () => {
    return (
        <UserProvider>
            <Routes>
                <Route path={"/"} element={<Header/>}/>
                <Route path="/register" element={<SignUp/>}/>
                <Route path={"/login"} element={<SignIn/>}/>
            </Routes>
        </UserProvider>
    );
};

export default App;
