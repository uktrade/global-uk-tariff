import React, {useState} from "react";

import Modal from './modal.jsx';



const escapeRegExp = (string) => {
  return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); // $& means the whole matched string
}

const renderHighlightedContent = (filters, string) => {
    const filterRegex = new RegExp(`(${filters.map(escapeRegExp).join('|')})`, 'ig');

    const parts = string.split(filterRegex);

    return <>{
        parts.map(
            (part, index) => <span className={index % 2 === 0 ? null : "highlight"} key={index}>{part}</span>
        )
    }</>
}


const DataRow = (props) => {
    let ukTariffRate;
    const highlight = (string) => {
        return renderHighlightedContent(props.filter.split(' '), String(string))
    }
    const [modalOpen, setModalOpen] = useState(false);

    if (props.trade_remedy_applies && !props.cet_applies_until_trade_remedy_transition_reviews_concluded) {
        ukTariffRate = <>
            <span className="govuk-table__cell--trigger" onClick={() => {
                setModalOpen(!modalOpen)
            }}>See details</span>
            {modalOpen ?
                <Modal handleClick={() => setModalOpen(false)}>
                    <h3>A trade remedy applies to {highlight(props.commodity)} for goods arriving from specific countries</h3>
                    <p>UK Global Tariff rate: {highlight(props.ukgt_duty_rate)}</p>
                    <p>This will apply from 1 January 2021.</p>
                    <p>Read more about <a href="https://www.gov.uk/guidance/trade-remedies-transition-policy">trade
                        remedies</a>.</p>
                </Modal> : null}
        </>

    } else if (props.trade_remedy_applies && props.cet_applies_until_trade_remedy_transition_reviews_concluded) {
        ukTariffRate = <>
            <span className="govuk-table__cell--trigger" onClick={() => {
                setModalOpen(!modalOpen)
            }}>See details</span>
            {modalOpen ?
                <Modal handleClick={() => setModalOpen(false)}>
                    <h3>A trade remedy applies to {highlight(props.commodity)} for goods arriving from specific countries</h3>
                    <p>UK Global Tariff rate: {highlight(props.ukgt_duty_rate)}</p>
                    <p>Common External Tariff rate: {highlight(props.cet_duty_rate)} - this will continue to apply until
                        transition reviews of all products in scope of this measure have been completed. The UK Global
                        Tariff will then apply.</p>
                    <p>Read more about <a href="https://www.gov.uk/guidance/trade-remedies-transition-policy">trade
                        remedies</a>.</p>
                </Modal> : null}
        </>

    } else if (props.suspension_applies) {
        ukTariffRate = <>
            <span className="govuk-table__cell--trigger" onClick={() => {
                setModalOpen(!modalOpen)
            }}>See details</span>
            {modalOpen ?
                <Modal handleClick={() => setModalOpen(false)}>
                    <p>UK Global Tariff rate: {highlight(props.ukgt_duty_rate)}</p>
                    <p>An Autonomous Suspension applies, this will be reviewed in due course.</p>
                </Modal> : null}
        </>
    } else if (props.atq_applies) {
        ukTariffRate = <>
            <span className="govuk-table__cell--trigger" onClick={() => {
                setModalOpen(!modalOpen)
            }}>See details</span>
            {modalOpen ?
                <Modal handleClick={() => setModalOpen(false)}>
                    <p>UK Global Tariff rate: {highlight(props.ukgt_duty_rate)}</p>
                    <p>A New Autonomous Quota of 260,000 tons will apply to the following commodity codes: 1701 13 10 and 1701 14 10 from 1 Jan 2021, for 12 months, with an in quota rate of 0.00%.</p>
                    <p>This will be reviewed in line with the UK’s suspensions policy in due course.</p>
                </Modal> : null}
        </>
    } else {
        ukTariffRate = highlight(props.ukgt_duty_rate)
    }


    return <tr className="govuk-table__row"role="row">
        <td className="govuk-table__cell hs-cell">
            <span className="hs-cell__heading">{props.commodity.slice(0, 4)}</span><span
            className="hs-cell__subheading">{props.commodity.slice(4, 6)}</span><span
            className="hs-cell__subheading">{props.commodity.slice(6, 8)}</span>{props.commodity.length > 8 ? <span
            className="hs-cell__subdivision">{props.commodity.slice(8)}</span> : null}
        </td>
        <td className="govuk-table__cell">{highlight(props.description)}</td>
        <td className="govuk-table__cell">{highlight(props.cet_duty_rate)}</td>
        <td className="govuk-table__cell">{ukTariffRate}</td>
        <td className="govuk-table__cell r">{highlight(props.change)}</td>
    </tr>
}


const DataTable = (props) => {
    return <table className="table table-hover govuk-table sticky dataTable no-footer" id="alltable" role="grid">
            <thead className="govuk-table__head">
            <tr className="govuk-table__row" role="row">
                <th className="nw govuk-table__header govuk-table__cell sorting_asc" style={{width: 104}}
                    rowSpan="1" colSpan="1" aria-label="Commodity">Commodity
                </th>
                <th className="nw govuk-table__header govuk-table__cell sorting_disabled" style={{width: 439}}
                    rowSpan="1" colSpan="1" aria-label="Description">Description
                </th>
                <th className="nw govuk-table__header govuk-table__cell sorting_disabled" style={{width: 181}}
                    rowSpan="1" colSpan="1" aria-label="Common External Tariff">Common External Tariff
                </th>
                <th className="nw govuk-table__header govuk-table__cell sorting_disabled" style={{width: 121}}
                    rowSpan="1" colSpan="1" aria-label="UK Global Tariff">UK Global Tariff
                </th>
                <th className="nw govuk-table__header r govuk-table__cell sorting_disabled" style={{width: 94}}
                    rowSpan="1" colSpan="1" aria-label="Change">Change
                </th>
            </tr>
            </thead>
            <tbody className="govuk-table__body">
            {
                props.rows.map(
                    (row, index) => <DataRow index={index} filter={props.filter} key={row.commodity + index} {...row} />
                )
            }
            </tbody>
        </table>
}

export default DataTable
