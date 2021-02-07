const Instagram = require('instagram-web-api')
const FileCookieStore = require('tough-cookie-filestore2')

const {INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD} = process.env

const cookieStore = new FileCookieStore('./cookies.json')
const client = new Instagram({username: INSTAGRAM_USERNAME, password: INSTAGRAM_PASSWORD , cookieStore})

const argv = process.argv.slice(2)

;(async () => {
	await client.login()
	
	const photo = argv[0]
	const caption = argv[1]

	await client.uploadPhoto({ photo, caption: caption, post: 'feed' })
})()
