import get-links
import visit-pages
import process-data

MAX_N_PAGES_FOR_LINKS = 26
MAX_N_PAGES_FOR_CHORDS = 500

get-links.main(MAX_N_PAGES_FOR_LINKS)
visit-pages.main(MAX_N_PAGES_FOR_CHORDS)
process-data(MAX_N_PAGES_FOR_CHORDS)