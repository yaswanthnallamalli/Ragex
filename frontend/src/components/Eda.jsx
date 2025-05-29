import React, { useState } from 'react';
import axios from 'axios';
import './Service3.css'; // Import the CSS file

const Service3 = () => {
    const [files, setFiles] = useState([]);
    const [dataInfo, setDataInfo] = useState(null);
    const [error, setError] = useState(null);

    const handleFileChange = (event) => {
        setFiles(event.target.files);
    };

    const handleUpload = async () => {
        const formData = new FormData();
        for (let i = 0; i < files.length; i++) {
            formData.append('files', files[i]);
        }

        try {
            const response = await axios.post('http://127.0.0.1:5000/api/upload', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            });
            setDataInfo(response.data);
            setError(null);
        } catch (error) {
            setError(error.response ? error.response.data.error : 'Error uploading files');
            setDataInfo(null);
        }
    };

    const handleGenerateGraphs = () => {
        window.location.href = 'http://localhost:8501/';
    };

    const renderTable = (data) => {
        return (
            <table className="table-auto w-full text-white">
                <thead>
                    <tr>
                        {Object.keys(data[0]).map((key) => (
                            <th key={key} className="px-4 py-2 border">{key}</th>
                        ))}
                    </tr>
                </thead>
                <tbody>
                    {data.map((row, index) => (
                        <tr key={index}>
                            {Object.values(row).map((value, i) => (
                                <td key={i} className="px-4 py-2 border">{value}</td>
                            ))}
                        </tr>
                    ))}
                </tbody>
            </table>
        );
    };

    return (
        <div className="flex flex-col min-h-screen text-white relative">
            <header className="py-12 md:py-16 lg:py-20 bg-[#000038] w-full">
                <div className="max-w-4xl mx-auto px-4 relative">
                    <h2 className="text-2xl md:text-3xl lg:text-4xl font-bold mb-6 text-teal-500">Exploratory Data Analysis (EDA) Summary</h2>
                    <input type="file" multiple onChange={handleFileChange} />
                    <div className="flex space-x-4 mt-4">
                        <button onClick={handleUpload} className="bg-teal-500 text-white px-6 py-3 rounded-lg hover:bg-teal-700 transition duration-300">
                            Upload and Analyze
                        </button>
                    </div>
                    {error && <p className="text-red-500 mt-4">{error}</p>}
                    {dataInfo && (
                        <div className="mt-6">
                            <h3 className="text-xl font-bold mb-4 text-teal-500">Combined Data Information</h3>
                            <p>Number of Rows: {dataInfo.num_rows}</p>
                            <p>Number of Columns: {dataInfo.num_columns}</p>
                            <h4 className="text-lg font-semibold mt-4">Columns and Data Types:</h4>
                            {renderTable(Object.entries(dataInfo.columns).map(([key, value]) => ({ Column: key, Type: value })))}
                            <h4 className="text-lg font-semibold mt-4">Summary Statistics:</h4>
                            {typeof dataInfo.summary_statistics === 'string' ? (
                                <p>{dataInfo.summary_statistics}</p>
                            ) : (
                                renderTable(Object.entries(dataInfo.summary_statistics).map(([key, value]) => ({ Statistic: key, ...value })))
                            )}
                            <h4 className="text-lg font-semibold mt-4">Missing Values:</h4>
                            {renderTable(Object.entries(dataInfo.missing_values).map(([key, value]) => ({ Column: key, 'Missing Values': value })))}
                            <div className="center-button-container mt-4">
                                <button onClick={handleGenerateGraphs} className="bg-teal-500 text-white px-6 py-3 rounded-lg hover:bg-teal-700 transition duration-300">
                                    Generate Graphs
                                </button>
                            </div>
                        </div>
                    )}
                </div>
            </header>
        </div>
    );
};

export default Service3;