import React from "react";


const Modal = (props) => {
    return <>
        <div className="govuk-table__cell--modal-closer" onClick={props.handleClick} />
        <div className="govuk-table__cell--modal nohover with-buttons">
            {props.children}
            <button className="govuk-button govuk-button--secondary govuk-table__cell--modal-button" data-module="govuk-button" onClick={props.handleClick}>
                Close
            </button>
        </div>
    </>
}

export default Modal;
