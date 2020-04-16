import React from "react";

const FilterOptions = (props) => {
    let sampleSize = props.sampleSize;
    let searchImage = props.searchImage;
    let filter = props.filter;

    const handleSubmit = (event) => {
        event.preventDefault()
    };

    return <form className="data-options" action="" method="get" onSubmit={handleSubmit}>
        <div className="data-options__filter">
            <div>
                <input type="search"
                       name="filter"
                       className="govuk-input"
                       placeholder="Search here..."
                       value={filter}
                       aria-controls="alltable"
                       onChange={props.handleFilterChange}/>
                <button type="submit">
                    <img src={searchImage} alt="search"/>
                </button>
            </div>
        </div>
        <div className="data-options__length">
            <label>Show&nbsp;
                <select name="n"
                        aria-controls="alltable"
                        className="govuk-select"
                        defaultValue={sampleSize}
                        onChange={props.handleSampleSizeChange}>
                    {[10, 25, 50, 100].map(
                        value => <option value={value} key={value}>{value}</option>)}
                </select>
                &nbsp;commodities
            </label>
        </div>
    </form>
}

export default FilterOptions;
