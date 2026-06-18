export default async function handler(req, res) {
    try {
        const response = await fetch('https://fix-kraft.onrender.com/api/sitemap.xml');
        const xml = await response.text();
        res.setHeader('Content-Type', 'application/xml');
        res.status(200).send(xml);
    } catch (error) {
        res.status(500).send('Error fetching sitemap');
    }
}