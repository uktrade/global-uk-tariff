import React from "react";

const Pagination = (props) => {
    const page = props.page;

    const setPage = (newPage) => {
        return (event) => {
            event.preventDefault();
            props.setPage(newPage);
        }
    }

    const renderOption = (pageOption, index) => {
        return pageOption === page ?
            <span className="pagination__links--button number selected"
                  aria-controls="alltable"
                  tabIndex="0"
                  key={pageOption + index}>{pageOption}</span> :
            pageOption === '...' ?
                <span className="pagination__links--button ellipsis" key={pageOption + index}>{pageOption}</span> :
                <a href=""
                   onClick={setPage(pageOption)}
                   className="pagination__links--button number"
                   aria-controls="alltable"
                   tabIndex="0"
                   key={pageOption + index}>{pageOption}</a>;
    }

    return <div className="pagination">
        <div className="pagination__info" role="status" aria-live="polite">
            <span className="govuk-body">Showing {props.start} to {props.end} of {props.total} commodities</span>
        </div>
        <div className="pagination__links">
            {page > 1 ?
                <a href=""
                   onClick={setPage(page - 1)}
                   className="pagination__links--button text"
                   aria-controls="alltable"
                   data-dt-idx="0"
                   tabIndex="-1">Previous</a> : null
            }
            {props.pageOptions.map(renderOption)}
            {page < (props.total / props.sampleSize) ?
                <a href=""
                   onClick={setPage(page + 1)}
                   className="pagination__links--button text"
                   aria-controls="alltable"
                   data-dt-idx="7"
                   tabIndex="0">Next</a> : null
            }
        </div>
    </div>
}

export default Pagination;
