/* Display leaflet map in NextJS */
/* https://medium.com/@tomisinabiodun/displaying-a-leaflet-map-in-nextjs-85f86fccc10c */

import dynamic from 'next/dynamic';

const ShipMap = dynamic(() => import('./ShipMapComponent'), { ssr: false });

export default ShipMap;