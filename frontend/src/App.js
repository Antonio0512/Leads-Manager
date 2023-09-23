import {UserProvider} from "./context/UserContext";
import {Route, Routes} from "react-router-dom";
import {SignUp} from "./components/SignUp";
import {Header} from "./components/Header";
import {SignIn} from "./components/SignIn";
import {LeadProvider} from "./context/LeadContext";
import {Table} from "./components/Table";

const App = () => {
    return (
        <UserProvider>
            <LeadProvider>
                <Header>
                    <Routes>
                        <Route path="/register" element={<SignUp/>}/>
                        <Route path={"/login"} element={<SignIn/>}/>
                        <Route path={"/leads"} element={<Table/>}/>
                    </Routes>
                </Header>
            </LeadProvider>
        </UserProvider>
    );
};

export default App;
