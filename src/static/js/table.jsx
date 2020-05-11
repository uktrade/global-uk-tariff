import React from "react";


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
    const highlight = (string) => {
        return renderHighlightedContent(props.filter.split(' '), String(string))
    }
    
    return <tr className="govuk-table__row"role="row">
        <td className="govuk-table__cell hs-cell">
            <span className="hs-cell__heading">{props.commodity.slice(0, 4)}</span><span
            className="hs-cell__subheading">{props.commodity.slice(4, 6)}</span><span
            className="hs-cell__subheading">{props.commodity.slice(6, 8)}</span>{props.commodity.length > 8 ? <span
            className="hs-cell__subdivision">{props.commodity.slice(8)}</span> : null}
        </td>
        <td className="govuk-table__cell">{highlight(props.description)}</td>
        <td className="govuk-table__cell nw">{highlight(props.cet_duty_rate)}</td>
        <td className="govuk-table__cell nw">{highlight(props.ukgt_duty_rate)}</td>
        <td className="govuk-table__cell r">{highlight(props.change)}</td>
    </tr>
}


const DataTable = (props) => {
    return <table className="table table-hover govuk-table sticky dataTable no-footer" id="alltable" role="grid"
               aria-describedby="alltable_info" style={{width: 1024}}>
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
