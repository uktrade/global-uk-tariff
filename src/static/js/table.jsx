import React from "react";


const escapeRegExp = (string) => {
  return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); // $& means the whole matched string
}

const renderHighlightedContent = (filter, string) => {
    const filterRegex = new RegExp(`(${escapeRegExp(filter)})`, 'ig');

    const parts = string.split(filterRegex);

    return <>{
        parts.map(
            (part, index) => <span className={index % 2 === 0 ? null : "highlight"} key={index}>{part}</span>
        )
    }</>
}


const DataTable = (props) => {
    const highlight = (string) => {
        return renderHighlightedContent(props.filter, string)
    }
    const renderRow = (row, index) => {
        return <tr className="govuk-table__row"role="row" key={row.commodity + index}>
            <td className="govuk-table__cell hs-cell">
                <span className="hs-cell__heading">{row.commodity.slice(0, 4)}</span><span
                className="hs-cell__subheading">{row.commodity.slice(4, 6)}</span><span
                className="hs-cell__subheading">{row.commodity.slice(6)}</span>
            </td>
            <td className="govuk-table__cell">{highlight(row.description)}</td>
            <td className="govuk-table__cell nw">{highlight(row.cet_duty_rate)}</td>
            <td className="govuk-table__cell nw">{highlight(row.ukgt_duty_rate)}</td>
            <td className="govuk-table__cell r">{highlight(row.change)}</td>
        </tr>
    }
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
                props.rows.map(renderRow)
            }
            </tbody>
        </table>
}

export default DataTable
