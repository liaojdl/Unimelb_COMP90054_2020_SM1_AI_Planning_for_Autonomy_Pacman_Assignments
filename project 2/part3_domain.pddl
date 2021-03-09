;; by Jiawei Liao 756560 
;; 1st May 2020
;; COMP90054-2020-SM1-a2
;; liao2@student.unimelb.edu

(define
    (domain pacman_hard)
    (:requirements :strips :typing :equality :adl)


    (:types
        physical_object location - object
        consumable_object Empty - physical_object
        Ghost Food Capsule - consumable_object
        cell - location
    )
    
    (:predicates
        ;; move from one cell to another
        (move ?from ?to - cell)
        ;; the location of Pacman
        (at ?loc - cell)
        ;; two connected cells are next to each other (left,right,top,bottom)
        (connected ?from ?to - cell)
        ;; What is the the cell, either food, ghost or empty
        (Incell ?loc - cell ?obj - physical_object)
        ;; whether the player is buffed by capsule
        ;; stage 2
        (buffed2 ?C - Capsule)
        ;; stage 1
        (buffed1 ?C - Capsule) 
    )
    

    (:action move
        :parameters (?cell1 ?cell2 - cell) 
        :precondition (and
            ;; can only move to cell2 if cell1 and cell 2 are connected 
            (at ?cell1 )
            (connected ?cell1 ?cell2)
            ;; can only move when at least one food exists
            (exists (?ce - cell) 
                (exists (?F - Food)
                    (Incell ?ce ?F)
                )
            )
            (or 
                ;; Check the buff for consuming a ghost
                (exists (?G - Ghost) 
                    (exists (?C - Capsule)
                        (and (Incell ?cell2 ?G) (buffed2 ?C) )
                    )
                )
                (exists (?G - Ghost) 
                    (exists (?C - Capsule)
                        (and (Incell ?cell2 ?G) (buffed1 ?C) )
                    )
                )
                ;; trivial case otherwise
                (exists (?G - Ghost)
                    (not (Incell ?cell2 ?G))
                )
            )  
        )

        :effect (and 
            (at ?cell2)
            (not (at ?cell1))
            ;; 1. clears original consumable object in cell 2
            (forall (?con - consumable_object) 
                (forall (?E - Empty)
                    (when (and (Incell ?cell2 ?con))
                        (and (Incell ?cell2 ?E) (not (Incell ?cell2 ?con)))
                    )
                )    
            )
            
            ;; 2. refresh capsule power duration to 2 steps if 
            ;; consuming a cell
            (forall (?C - Capsule) 
                (when
                    (and (Incell ?cell2 ?C))
                    (and (buffed2 ?C))
                )
            )
            ;; one step of the two power levels used
            (forall (?C - Capsule) 
                (when (and (not (Incell ?cell2 ?C)) (buffed2 ?C))
                    (and (not (buffed2 ?C)) (buffed1 ?C) )
                )
            )
            ;; all power used up, no longer buffed by capsule
            (forall (?C - Capsule) 
                (when (and (not (Incell ?cell2 ?C)) (buffed1 ?C))
                    (and (not (buffed2 ?C)) (not (buffed1 ?C)))
                )
            )
        )
    )
)