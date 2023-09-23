import {UserProvider} from "./context/UserContext";
import {Route, Routes} from "react-router-dom";
import {SignUp} from "./components/SignUp";
import {Header} from "./components/Header";
import {SignIn} from "./components/SignIn";
import {LeadProvider} from "./context/LeadContext";
import {Table} from "./components/Table";
import {AuthRouteGuard} from "./routeGuards/userAuthGuard";
import {HomePage} from "./components/HomePage";

const App = () => {
    return (
        <UserProvider>
            <LeadProvider>
                <Header>
                    <Routes>
                        <Route path={"/"} element={<HomePage/>}/>
                        <Route path="/register" element={<SignUp/>}/>
                        <Route path={"/login"} element={<SignIn/>}/>
                        <Route element={<AuthRouteGuard/>}>
                            <Route path={"/leads"} element={<Table/>}/>
                        </Route>
                    </Routes>
                </Header>
            </LeadProvider>
        </UserProvider>
    );
};

export default App;
