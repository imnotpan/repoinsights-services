nod = """
    SELECT
        c.project_id,
        COUNT(DISTINCT c.author_id) AS number_of_developers
    FROM
        ghtorrent_restore_2015.commits c
    JOIN 
        ghtorrent_restore_2015.projects pr
    ON 
        c.project_id = pr.id
    WHERE 
        pr.id = %s
    GROUP BY
        pr.name, c.project_id
    ORDER BY 
        number_of_developers DESC;
    """
