import * as React from 'react';
import { createRoot } from 'react-dom/client';
import OperationBallotBoxFliers from "./OperationBallotBoxFliers";

const container = document.getElementById('obb-fliers');

if (container === null || container === undefined) {
    throw new Error('Could not find root element');
}

const root = createRoot(container);

// @ts-ignore
root.render(<OperationBallotBoxFliers />);