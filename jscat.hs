import System.Environment
import Data.List as L

main :: IO()
main = getArgs >>= (\x -> readFile (head x) >>= outJSfiles)

isJS :: String -> Bool
isJS str = isInfixOf sub str
  where 
    sub = ".js"::String

prune :: String -> String
prune s = drop 9 s

getJSlist :: String -> [String]
getJSlist s = sort (L.nub $ map prune (filter isJS $ words s))

outJSfiles :: String -> IO()
outJSfiles s = putStrLn (unlines $ getJSlist s)
