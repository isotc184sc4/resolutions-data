import { ref, type Ref } from 'vue'
import FlexSearch from 'flexsearch'

const BUILD_TIME = Date.now()

export interface Action {
  type: string
  subject?: string
  message: string
  dates?: any[]
}

export interface Consideration {
  type: string
  message: string
  dates?: any[]
}

export interface Approval {
  type: string
  degree: string
  message?: string
}

export interface Resolution {
  id: string
  title: string
  subject: string
  year: string
  venue: string
  source_file: string
  source_title: string
  source_type?: string
  group_id?: string
  meeting_date: string
  is_acclamation: boolean
  actions: Action[]
  considerations: Consideration[]
  approvals: Approval[]
  categories?: string[]
  dates: any[]
  snippet: string
  urn?: string
  meeting_urn?: string
}

const resolutions = ref<Resolution[]>([]) as Ref<Resolution[]>
const isLoaded = ref(false)

let indexInstance: InstanceType<typeof FlexSearch.Document> | null = null
let loadPromise: Promise<void> | null = null

export function useResolutions() {
  const loadData = async () => {
    if (isLoaded.value) return
    if (loadPromise) { await loadPromise; return }

    loadPromise = (async () => {
      try {
        const response = await fetch(`${import.meta.env.BASE_URL}data/resolutions.json?t=${BUILD_TIME}`)
        const data: Resolution[] = await response.json()
        resolutions.value = data

        const idx = new FlexSearch.Document({
          document: {
            id: 'internalId',
            index: ['id', 'title', 'subject', 'snippet']
          },
          tokenize: 'forward'
        })

        data.forEach((res, i) => {
          idx.add({
            internalId: i,
            id: res.id,
            title: res.title,
            subject: res.subject,
            snippet: res.snippet
          })
        })

        indexInstance = idx
        isLoaded.value = true
      } catch (e) {
        console.error('Failed to load resolutions', e)
        loadPromise = null
      }
    })()

    await loadPromise
  }

  const search = (query: string): Set<number> => {
    if (!indexInstance || !query) return new Set()
    const results = indexInstance.search(query, { limit: 1000 })
    const matched = new Set<number>()
    results.forEach((fieldResult: any) => {
      fieldResult.result.forEach((docId: number) => {
        matched.add(docId)
      })
    })
    return matched
  }

  return {
    resolutions,
    isLoaded,
    loadData,
    search
  }
}
