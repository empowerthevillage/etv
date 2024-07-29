import * as React from 'react';
import { pdfjs, Document, Page } from 'react-pdf';
import 'react-pdf/dist/esm/Page/AnnotationLayer.css';
import 'react-pdf/dist/esm/Page/TextLayer.css';

import './OperationBallotBoxFliers.css';

pdfjs.GlobalWorkerOptions.workerSrc = new URL(
    'pdfjs-dist/build/pdf.worker.min.mjs',
    import.meta.url,
).toString();

type PDFFile = string | File | null;

export default function OperationBallotBoxFliers() {

    return (
        <div className="Example">
            <div className="Example__container">
                <a href={'http://2024obb.s3-website.us-east-2.amazonaws.com/2024-OBB-Florida.pdf'}
                   download={"2024-OBB-Florida.pdf"} target={"_blank"}>
                    <Document file={'http://2024obb.s3-website.us-east-2.amazonaws.com/2024-OBB-Florida.pdf'}>
                        <Page pageNumber={1} width={375}/>
                    </Document>
                </a>
                <a href={'http://2024obb.s3-website.us-east-2.amazonaws.com/2024-OBB-Florida.pdf'}
                   download={"2024-OBB-Florida.pdf"} target={"_blank"}>
                    <Document file={'http://2024obb.s3-website.us-east-2.amazonaws.com/2024-OBB-Florida.pdf'}>
                        <Page pageNumber={1} width={375}/>
                    </Document>
                </a>
                <a href={'http://2024obb.s3-website.us-east-2.amazonaws.com/2024-OBB-Florida.pdf'}
                   download={"2024-OBB-Florida.pdf"} target={"_blank"}>
                    <Document file={'http://2024obb.s3-website.us-east-2.amazonaws.com/2024-OBB-Florida.pdf'}>
                        <Page pageNumber={1} width={375}/>
                    </Document>
                </a>
                <a href={'http://2024obb.s3-website.us-east-2.amazonaws.com/2024-OBB-Florida.pdf'}
                   download={"2024-OBB-Florida.pdf"} target={"_blank"}>
                    <Document file={'http://2024obb.s3-website.us-east-2.amazonaws.com/2024-OBB-Florida.pdf'}>
                        <Page pageNumber={1} width={375}/>
                    </Document>
                </a>
                <a href={'http://2024obb.s3-website.us-east-2.amazonaws.com/2024-OBB-Florida.pdf'}
                   download={"2024-OBB-Florida.pdf"} target={"_blank"}>
                    <Document file={'http://2024obb.s3-website.us-east-2.amazonaws.com/2024-OBB-Florida.pdf'}>
                        <Page pageNumber={1} width={375}/>
                    </Document>
                </a>
                <a href={'http://2024obb.s3-website.us-east-2.amazonaws.com/2024-OBB-Florida.pdf'}
                   download={"2024-OBB-Florida.pdf"} target={"_blank"}>
                    <Document file={'http://2024obb.s3-website.us-east-2.amazonaws.com/2024-OBB-Florida.pdf'}>
                        <Page pageNumber={1} width={375}/>
                    </Document>
                </a>
                <a href={'http://2024obb.s3-website.us-east-2.amazonaws.com/2024-OBB-Florida.pdf'}
                   download={"2024-OBB-Florida.pdf"} target={"_blank"}>
                    <Document file={'http://2024obb.s3-website.us-east-2.amazonaws.com/2024-OBB-Florida.pdf'}>
                        <Page pageNumber={1} width={375}/>
                    </Document>
                </a>
                <a href={'http://2024obb.s3-website.us-east-2.amazonaws.com/2024-OBB-Florida.pdf'}
                   download={"2024-OBB-Florida.pdf"} target={"_blank"}>
                    <Document file={'http://2024obb.s3-website.us-east-2.amazonaws.com/2024-OBB-Florida.pdf'}>
                        <Page pageNumber={1} width={375}/>
                    </Document>
                </a>
                <a href={'http://2024obb.s3-website.us-east-2.amazonaws.com/2024-OBB-Florida.pdf'}
                   download={"2024-OBB-Florida.pdf"} target={"_blank"}>
                    <Document file={'http://2024obb.s3-website.us-east-2.amazonaws.com/2024-OBB-Florida.pdf'}>
                        <Page pageNumber={1} width={375}/>
                    </Document>
                </a>
                <a href={'http://2024obb.s3-website.us-east-2.amazonaws.com/2024-OBB-Florida.pdf'}
                   download={"2024-OBB-Florida.pdf"} target={"_blank"}>
                    <Document file={'http://2024obb.s3-website.us-east-2.amazonaws.com/2024-OBB-Florida.pdf'}>
                        <Page pageNumber={1} width={375}/>
                    </Document>
                </a>
                <a href={'http://2024obb.s3-website.us-east-2.amazonaws.com/2024-OBB-Florida.pdf'}
                   download={"2024-OBB-Florida.pdf"} target={"_blank"}>
                    <Document file={'http://2024obb.s3-website.us-east-2.amazonaws.com/2024-OBB-Florida.pdf'}>
                        <Page pageNumber={1} width={375}/>
                    </Document>
                </a>
                <a href={'http://2024obb.s3-website.us-east-2.amazonaws.com/2024-OBB-Florida.pdf'}
                   download={"2024-OBB-Florida.pdf"} target={"_blank"}>
                    <Document file={'http://2024obb.s3-website.us-east-2.amazonaws.com/2024-OBB-Florida.pdf'}>
                        <Page pageNumber={1} width={375}/>
                    </Document>
                </a>
                <a href={'http://2024obb.s3-website.us-east-2.amazonaws.com/2024-OBB-Florida.pdf'}
                   download={"2024-OBB-Florida.pdf"} target={"_blank"}>
                    <Document file={'http://2024obb.s3-website.us-east-2.amazonaws.com/2024-OBB-Florida.pdf'}>
                        <Page pageNumber={1} width={375}/>
                    </Document>
                </a>
                <a href={'http://2024obb.s3-website.us-east-2.amazonaws.com/2024-OBB-Florida.pdf'}
                   download={"2024-OBB-Florida.pdf"} target={"_blank"}>
                    <Document file={'http://2024obb.s3-website.us-east-2.amazonaws.com/2024-OBB-Florida.pdf'}>
                        <Page pageNumber={1} width={375}/>
                    </Document>
                </a>
            </div>
        </div>
    );
}