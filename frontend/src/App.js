import {useEffect, useState} from "react";

const App = () => {
    const [message, setMessage] = useState("");

    const getWelcomeMessage = async () => {
        const requestOptions = {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
            },
        };
        const response = await fetch("/api", requestOptions);
        const data = await response.json();
        console.log(data);

        if (!response.ok) {
            setMessage("Something went wrong :(");
        } else {
            setMessage(data)
        }
    };

    useEffect(() => {
        getWelcomeMessage();
    }, [])
    return (
        <div>
            <h1>{message}</h1>
        </div>
    );
};

export default App;
