import {useState} from "react";
import {createLead} from "../services/leadService";

export const LeadModal = ({active, handleModal, id, access_token, setError}) => {

    const initialFormData = {
        first_name: "",
        last_name: "",
        company: "",
        email: "",
        note: "",
    }

    const [formData, setFormData] = useState(initialFormData);

    const {first_name, last_name, company, email, note} = formData;

    const onChange = (e) => setFormData({...formData, [e.target.name]: e.target.value});

    const cleanFormData = () => {
        setFormData(initialFormData);
    };

    const onSubmit = async (e) => {
        e.preventDefault();

        try {
            await createLead(formData, access_token);
            cleanFormData();
            handleModal();
        } catch (error) {
            setError(error);
        }
    };

    return (
        <div className={`modal ${active && "is-active"}`}>
            <div className="modal-background" onClick={handleModal}></div>
            <div className="modal-card">
                <header className="modal-card-head has-background-primary-light">
                    <h1 className="modal-card-title">
                        {id ? "Update Lead" : "Create Lead"}
                    </h1>
                </header>
                <section className="modal-card-body">
                    <form>
                        <div className="field">
                            <label className="label" htmlFor="first_name">First Name</label>
                            <div className="control">
                                <input type="text"
                                       placeholder="Enter first name"
                                       id="first_name"
                                       name="first_name"
                                       value={first_name}
                                       onChange={(e) => onChange(e)}
                                       className="input"
                                       required
                                       autoComplete="given-name"
                                />
                            </div>
                        </div>
                        <div className="field">
                            <label className="label" htmlFor="last_name">Last Name</label>
                            <div className="control">
                                <input type="text"
                                       placeholder="Enter last name"
                                       id="last_name"
                                       name="last_name"
                                       value={last_name}
                                       onChange={(e) => onChange(e)}
                                       className="input"
                                       required
                                       autoComplete="family-name"
                                />
                            </div>
                        </div>
                        <div className="field">
                            <label className="label" htmlFor="company">Company</label>
                            <div className="control">
                                <input type="text"
                                       placeholder="Enter company"
                                       id="company"
                                       name="company"
                                       value={company}
                                       onChange={(e) => onChange(e)}
                                       className="input"
                                       required
                                       autoComplete="organization"
                                />
                            </div>
                        </div>
                        <div className="field">
                            <label className="label" htmlFor="email">Email</label>
                            <div className="control">
                                <input type="text"
                                       placeholder="Enter email"
                                       id="email"
                                       name="email"
                                       value={email}
                                       onChange={(e) => onChange(e)}
                                       className="input"
                                       required
                                       autoComplete="email"
                                />
                            </div>
                        </div>
                        <div className="field">
                            <label className="label" htmlFor="note">Note</label>
                            <div className="control">
                                <input type="text"
                                       placeholder="Enter note"
                                       id="note"
                                       name="note"
                                       value={note}
                                       onChange={(e) => onChange(e)}
                                       className="input"
                                       autoComplete="off"
                                />
                            </div>
                        </div>
                    </form>
                </section>
                <footer className="modal-card-foot has-background-primary-light">
                    {id ?
                        (<button className="button is-info">Update</button>)
                        :
                        (<button className="button is-primary" onClick={(e) => onSubmit(e)}>Create</button>)
                    }
                    <button className="button" onClick={handleModal}>Cancel</button>
                </footer>
            </div>
        </div>
    );
};