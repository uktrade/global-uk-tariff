import React, {useEffect, useState} from "react";
import ReactDOM from 'react-dom';

import DataTable from './table.jsx';
import FilterOptions from './filterOptions.jsx';
import Pagination from './pagination.jsx';


const getPageOptions = (startPage, maxPage, pageRange = 2) => {
    const minPage = 1;

    let pageOptions = [];

    for (let i = startPage - pageRange; i < startPage + pageRange + 1; i++) {
        if (0 < i && i < maxPage) {
            pageOptions.push(i);
        }
    }

    if (pageOptions.length === 0) { // edge case where there are no results.
        return [1]
    }

    if (!pageOptions.includes(minPage)){
        pageOptions = [minPage, '...'].concat(pageOptions);
    }

    if (!pageOptions.includes(maxPage)){
        pageOptions = pageOptions.concat(['..', maxPage]);
    }

    return pageOptions
}

const updateURL = (filter, sampleSize, page) => {
    let updatedURL = window.location.protocol + "//"
        + window.location.host + window.location.pathname
        + `?filter=${filter}&n=${sampleSize}&p=${page}`;

    window.history.pushState({path: updatedURL}, '', updatedURL);
}


const FilterTable = (props) => {
    const data = props.data;

    const [page, setPage] = useState(props.page);
    const [filter, setFilter] = useState(props.filterOptions.filter);
    const [sampleSize, setSampleSize] = useState(props.filterOptions.sampleSize);

    const filteredData = data.filter(
        (row) => {
            return Object.values(row).some(item => String(item).toLowerCase().includes(filter.toLowerCase()))
        }
    )
    const displayData = filteredData.slice((page - 1) * sampleSize, page * sampleSize);

    const startRecord = displayData.length !== 0 ? (sampleSize * (page - 1)) + 1 : 0;
    const endRecord = sampleSize * (page) < filteredData.length ? sampleSize * (page) : filteredData.length;
    const pageOptions = getPageOptions(page, Math.ceil(filteredData.length / sampleSize));

    const handleFilterChange = (event) => {
        setFilter(event.target.value);
        setPage(1);
        updateURL(event.target.value, sampleSize, 1)
    };

    const handleSampleSizeChange = (event) => {
        setSampleSize(event.target.value);
        setPage(1);
        updateURL(filter, event.target.value, 1)
    }

    const handlePageChange = (newPage) => {
        setPage(newPage);
        updateURL(filter, sampleSize, newPage);
    }

    return <div id="alltable_wrapper" className="dataTables_wrapper no-footer">
        <FilterOptions handleSampleSizeChange={handleSampleSizeChange}
                       handleFilterChange={handleFilterChange}
                       filter={filter}
                       sampleSize={sampleSize}
                       searchImage={props.filterOptions.searchImage} />
        <br />
        <br />
        <div className="govuk-body">If you need help finding your commodity code you can use the <a
            href="https://www.gov.uk/guidance/using-the-trade-tariff-tool-to-find-a-commodity-code"
            className="govuk-link govuk-link--no-visited-state">trade tariff tool</a>.
        </div>

        <DataTable rows={displayData} filter={filter}/>

        <Pagination start={startRecord}
                    end={endRecord}
                    page={page}
                    sampleSize={sampleSize}
                    total={filteredData.length}
                    pageOptions={pageOptions}
                    setPage={handlePageChange}/>

        <div className="dt-buttons">
            <a href={`/api/global-uk-tariff.csv?filter=${filter}`}
               className="dt-button govuk-button buttons-csv buttons-html5" tabIndex="0" aria-controls="alltable"
               type="button">
                Export to CSV
            </a>
            <a href={`/api/global-uk-tariff.xlsx?filter=${filter}`}
               className="dt-button govuk-button buttons-excel buttons-html5" tabIndex="0" aria-controls="alltable"
               type="button">
                Export to Excel
            </a>
        </div>
    </div>
};

const renderFilterTable = (elementId, sampleSize, page, filter, searchImage, data, pageOptions) => {
    const filterOptions = {
        searchImage: searchImage,
        sampleSize: sampleSize,
        filter: filter
    };

    return ReactDOM.render(
            <FilterTable data={data}
                         page={page}
                         pageOptions={pageOptions}
                         filterOptions={filterOptions} />,
            document.getElementById(elementId)
        )
};

window.renderFilterTable = renderFilterTable;
