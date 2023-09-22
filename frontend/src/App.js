import {UserProvider} from "./context/UserContext";
import {Route, Routes} from "react-router-dom";
import {SignUp} from "./components/SignUp";

const App = () => {
    return (
        <UserProvider>
            <Routes>
                <Route path="/signup" element={<SignUp/>}/>
            </Routes>
        </UserProvider>
    );
};

export default App;
